# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import *
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout, authenticate

from django.urls import reverse

from django.db import transaction


from django.db.utils import IntegrityError


from .forms import *
import json
import math
import random
import html
import os
import requests

import configparser
config = configparser.ConfigParser()
config.read('conf.ini')
# MAPBOX_ACCESS_TOKEN = config['TOKENS']['mapbox'] if not os.environ.get('MAPBOX_ACCESS_TOKEN') else os.environ.get('MAPBOX_ACCESS_TOKEN')
# PARTICLE_ACCESS_TOKEN = config['TOKENS']['particle'] if not os.environ.get('PARTICLE_ACCESS_TOKEN') else os.environ.get('PARTICLE_ACCESS_TOKEN')

from quiz.settings import MAPBOX_ACCESS_TOKEN, PARTICLE_ACCESS_TOKEN, MAPBOX_NO_LIMIT_ACCESS_TOKEN, BASE_DIR

from django.views.decorators.csrf import csrf_exempt


from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

import logging
logger = logging.getLogger('django.server')


import geojson
from geojson import Feature, Point, FeatureCollection, LineString, MultiLineString
import pandas as pd
import numpy as np

from scipy.spatial import distance_matrix



from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

class TrackerListJson(BaseDatatableView):
    model = TrackerChip
    columns = ['device_name', 'device_id', 'created_date']
    # define column names that will be used in sorting
    # order is important and should be same as order of columns displayed
    # non-sortable, use value like ''
    order_columns = ['device_name', 'device_id', 'created_date']
    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500

    def render_column(self, row, column):
        return super(TrackerListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(device_name__istartswith=search)
        return qs

    # "<a href='/shop/customer/%s/'>%s</a>" % (item.customer.id,item.customer.name),
    def prepare_results(self, qs):


        json_data = []
        for item in qs:



            item_link_html = "<a href='/tracker/%s'>%s</a>" % (item.id,item.device_name)


            json_data.append([
                item_link_html,
                item.device_id if item.device_id else '',
                item.created_date if item.created_date else '',
                # item.active if item.active else '',
            ])
        return json_data



class TripListJson(BaseDatatableView):
    model = Trip
    #AJAX error w orig dest
    columns = ['tracker', 'orig','dest', 'check_point',
               'check_point_time', 'active']

    order_columns = ['tracker', '','', 'check_point',
               'check_point_time', 'active']
    max_display_length = 500

    def render_column(self, row, column):
        if column == 'orig':
            # escape HTML for security reasons
            return escape(row.load.orig.city)
        elif column == 'dest':
            # escape HTML for security reasons
            return escape(row.load.dest.city)
        else:
            return super(TripListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(tracker__device_name__istartswith=search)
        return qs

    def prepare_results(self, qs):

        json_data = []
        for item in qs:
            # if customer_id:
            #     json_data.append([
            #         "<a href='/shop/crm/%s/'>%s</a>" % (item.id, item.erpid),
            #         item.state,
            #     ])
            # else:  # if shop_id:
            id = item.id
            name = item.tracker.device_name
            value = 'trip'+str(item.id)
            chkbox_html = '''<input type="checkbox" id="%s" 
            class = "trip_checkbox"
            name="%s" value="%s">
             <label for="%s"> %s</label> 
            '''%(id, name, value, name, name)


            json_data.append([
                chkbox_html,
                item.load.orig.city,
                item.load.dest.city,
                item.check_point.loc.city if item.check_point else '',
                item.check_point_time if item.check_point_time else '',
                item.active if item.active else '',
            ])
        return json_data


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/accounts/login/')
def index(request):


    context = { 'mapbox_token': MAPBOX_ACCESS_TOKEN}
    return render(request, 'geo/index.html', context)


## SET UP FOR WEBHOOK. Webhook should post events to url: "/<device_id>"
## Need to add event data to database and map to correct fields
@csrf_exempt
def events(request, device_id):
    # module = FencingModule.objects.get(device_id=device_id)
    if request.method == "POST":
        data = request.POST.dict()#logger.info(request.POST)
        logger.info(data)

        fencing_id = data.get('coreid')
        published_at = data.get('published_at')
        device_data = data.get('data')
        if device_data and fencing_id and published_at:
            device_data_dict = json.loads(device_data)
            tracker_name = device_data_dict.get('DeviceName')
            tracker_id = device_data_dict.get('DeviceID')
            rssi = device_data_dict.get('RSSI')

            logger.info('webhook POST %s %s %s %s %s' % (fencing_id,
                                                         published_at,
                                                         tracker_name,
                                                         tracker_id,
                                                         rssi))
            # webhook POST e00fce68aadec91d27441ac2 2020-09-26T19:21:20.266Z iBeacon420 -56

            fencing_module, c1 = FencingModule.objects.get_or_create(device_id = fencing_id)
            tracker_chip, c2 = TrackerChip.objects.get_or_create(device_name = tracker_name,
                                                                device_id = tracker_id)

            logger.info('MODELS %s %s %s %s'%(fencing_module.device_id, fencing_module.device_name,
                                              tracker_chip.device_id, tracker_chip.device_name))


            fake_load = Load.objects.all()[0]

            #TODO - get all active loads (trips) associated with the tracker, Trip

            # client = Client.objects.get(user = request.user) request.user is AnonymousUser

            fake_trips_to_update = Trip.objects.filter(load = fake_load, tracker = tracker_chip)

            for fake_trip_to_update in fake_trips_to_update:
                fake_trip_to_update.check_point = fencing_module
                fake_trip_to_update.check_point_time = published_at
                fake_trip_to_update.save()
                # device_data()

                fake_trip_to_update.update_fencing()


        '''
        
         {'event': 'tracking_event', 
         'data': '{ "DeviceName": "iBeacon420", "RSSI": -60 }', 
         'published_at': '2020-09-26T18:35:47.942Z', 
         'coreid': 'e00fce68aadec91d27441ac2'}
         
         
[26/Sep/2020 17:50:04,474] <QueryDict: {'event': ['tracking_event'], 
'data': ['{ "DeviceName": "iBeacon420",   <----on the load TrackingChip.device_name
"RSSI": -60 }'], 
'published_at': ['2020-09-26T17:50:03.665Z'], 
'coreid': ['e00fce68aadec91d27441ac2']}>   <-----on the side of the road  (where we are getting informatuon from)   FencingModule.device_id
        '''

        # logger.info('webhook post type %s'%type(data))

    return JsonResponse({'ok': 'ok'}, safe=False)


def add_trip(request):
    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TripForm(request.POST, user = request.user)#request.POST, instance=trip_obj, user = request.user)

        if form.is_valid():
            client = Client.objects.get(user = request.user)

            cd = form.cleaned_data

            orig_id, dest_id, ref = cd['orig_id'], cd['dest_id'], cd['ref']
            load, c=Load.objects.get_or_create(orig_id=orig_id,
                                               dest_id=dest_id,
                                               ref1=ref, client=client)

            tracker_chips = cd['tracker_select']

            for tc in tracker_chips:
                trip, c = Trip.objects.get_or_create(load=load,
                                                     tracker=tc,
                                                     client=client)


            # saved = form.save()
            return HttpResponseRedirect(reverse('index'))#'tracker', args=[saved.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TripForm(user = request.user)#instance=trip_obj, user = request.user)
    context = {'form': form}
    return render(request, 'geo/add_trip_detail.html', context)


def edit_trip(request, d_id=None):
    HttpResponse('ok')

def tracker(request, d_id=None):
    # if this is a POST request we need to process the form data
    if d_id:
        tracker_obj = TrackerChip.objects.get(pk=d_id)
    else:
        tracker_obj = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TrackerForm(request.POST, instance=tracker_obj)
        # check whether it's valid:
        if not tracker_obj:
            client = Client.objects.get(user = request.user)
            form.fields['client'].initial = client#.id

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            saved = form.save()
            return HttpResponseRedirect(reverse('tracker', args=[saved.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TrackerForm(instance=tracker_obj)
    context = {'tracker': tracker_obj, 'form': form}
    return render(request, 'geo/tracker_detail.html', context)



@csrf_exempt
def add_trip_to_map(request):
    trip_id = request.POST['trip_id']
    trip_ids = json.loads(request.POST['trip_ids'])

    data = []
    endpoint_dump = []

    features = []

    for trip_id in trip_ids:

        trip = Trip.objects.get(pk = trip_id)

        # directions = trip.load.no_limit_directions()
        directions=trip.no_limit_directions()

        coordinates = directions['routes'][0]['geometry']['coordinates']

        # orig, dest = trip.load.orig, trip.load.dest

        trip_route = Feature(geometry=LineString(coordinates))#[(8.919, 44.4074), (8.923, 44.4075)])

        features.append(trip_route)

        # coord = {'orig_lat':str(orig.lat),
        #         'orig_lon':str(orig.lon),
        #         'dest_lat':str(dest.lat),
        #         'dest_lon':str(dest.lon)}

        endpoint_coords = trip.get_endpoints()
        endpoint_dump.append(endpoint_coords)

    feature_collection = FeatureCollection(features)

    return HttpResponse(json.dumps({'endpoints': endpoint_dump, 'features': feature_collection}))#json.dumps(feature_collection))



@csrf_exempt
def add_fencing(request):
    '''

    Might be able to get other locations from http://www.poi-factory.com/ , etc
    :param request:
    :return:
    '''
    marker_dump = []

    trip_ids = json.loads(request.POST['trip_ids'])

    for trip_id in trip_ids:

        trip = Trip.objects.get(pk = trip_id)
        marker_dump+=trip.get_fencing()


    return HttpResponse(json.dumps({'markers': marker_dump}))#json.dumps(feature_collection))

@csrf_exempt
def loc_autocomplete(request):
    resp_data = []

    if request.is_ajax():
        locs=Location.objects.all()
        q = request.GET.get('term', '')
        locs = locs.filter(city__icontains=q)  # [:20]#(dispname__icontains = q )[:20]

        for loc in locs:
            json_id = loc.id
            json_label = '%s, %s'%(loc.city, loc.state)  # dispname
            json_value = loc.city  # dispname
            resp_data.append({'id': json_id, 'label': json_label, 'value': json_value})


    return JsonResponse(resp_data, safe=False)

@login_required(login_url='/accounts/login/')
def manage_trackers(request):
    context = {'mapbox_token': MAPBOX_ACCESS_TOKEN}
    return render(request, 'geo/manage_trackers.html', context)

@login_required(login_url='/accounts/login/')
def manage_trips(request):
    context = {'mapbox_token': MAPBOX_ACCESS_TOKEN}
    return render(request, 'geo/manage_trips.html', context)