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
MAPBOX_ACCESS_TOKEN = config['TOKENS']['mapbox'] if not os.environ.get('MAPBOX_ACCESS_TOKEN') else os.environ.get('MAPBOX_ACCESS_TOKEN')
PARTICLE_ACCESS_TOKEN = config['TOKENS']['particle'] if not os.environ.get('PARTICLE_ACCESS_TOKEN') else os.environ.get('PARTICLE_ACCESS_TOKEN')


from django.views.decorators.csrf import csrf_exempt


from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

import logging
logger = logging.getLogger('django.server')



# from spyrk import SparkCloud
# spark = SparkCloud(PARTICLE_ACCESS_TOKEN)
# tracker_dict = {}
# for fm in fencing_modules:
#     for s in spark.devices:
#         if fm == s:
#             tracker_dict[spark.devices[s].Name] = {"Time": spark.devices[s].Time,
#                                                    "CheckPoint_Name": fm,
#                                                    "CheckPoint_DeviceID": spark.devices[s].id,
#                                                    "CheckPoint_Location": fencing_modules[fm]
#                                                    }
# print(tracker_dict)




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


class LoadListJson(BaseDatatableView):
    model = Load
    columns = ['ref1_type', 'ref1', 'orig', 'dest']

    order_columns = ['ref1_type', 'ref1', 'orig', 'dest']
    max_display_length = 500

    def render_column(self, row, column):
        return super(LoadListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(ref1__istartswith=search)
        return qs


class TripListJson(BaseDatatableView):
    model = Trip
    columns = ['tracker', 'orig','dest', 'check_point',
               'check_point_time', 'active']

    order_columns = ['tracker', 'orig','dest', 'check_point',
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
        # prepare list with output column data
        # queryset is already paginated here
        # shop_id = self.kwargs.get('shop_id', None)
        # customer_id = self.kwargs.get('customer_id', None)
        # simple example:

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
                # "<a href='%s/'>%s</a>" % (item.id, item.tracker),
                chkbox_html,
                item.load.orig.city,
                item.load.dest.city,
                item.check_point if item.check_point else '',
                item.check_point_time if item.check_point_time else '',
                item.active if item.active else ''
            ])
        return json_data


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/accounts/login/')
def index(request):
    logger.info('log info Im on the index')
    logger.error('log error Im on the index')
    print('print Im on the index')
    tracker_dict = {}
    context = {'devices': tracker_dict, 'mapbox_token': MAPBOX_ACCESS_TOKEN}
    return render(request, 'geo/index.html', context)

def trackers(request):
    tracker_dict = {}
    context = {'devices': tracker_dict}
    return render(request, 'geo/trackers.html', context)


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
        if data and fencing_id and published_at:
            device_data_dict = json.loads(device_data)
            device_name = device_data_dict.get('DeviceName')
            rssi = device_data_dict.get('RSSI')

            logger.info('webhook post', fencing_id, published_at, device_name, rssi)


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

def loads(request):
    context = {}
    return render(request, 'geo/loads.html', context)


@csrf_exempt
def add_trip_to_map(request):
    trip_id = request.POST['trip_id']
    trip = Trip.objects.get(pk = trip_id)
    orig, dest = trip.load.orig, trip.load.dest
    data = {'orig_lat':str(orig.lat),
            'orig_lon':str(0-orig.lon),
            'dest_lat':str(dest.lat),
            'dest_lon':str(0-dest.lon)}
    return HttpResponse(json.dumps(data))


def api(request):
    '''
    This is for testing api stuff
    :param request:
    :return:
    '''

    #https://docs.mapbox.com/api/search/#geocoding

    url = "https://api.particle.io/v1/devices"

    payload = {}
    headers = {
        'Authorization': 'Bearer %s'%PARTICLE_ACCESS_TOKEN
    }

    devices_response = requests.request("GET", url, headers=headers, data=payload)
    for device_json in devices_response.json():

        print(device_json['name'], device_json)



    print(devices_response.text.encode('utf8'))

    return JsonResponse(devices_response.json(), safe=False)




