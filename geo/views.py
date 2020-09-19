# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import *
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout, authenticate

from django.urls import reverse


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
    columns = ['device_name', 'tracker_id', 'created_date']
    # define column names that will be used in sorting
    # order is important and should be same as order of columns displayed
    # non-sortable, use value like ''
    order_columns = ['device_name', 'tracker_id', 'created_date']
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
    columns = ['tracker', 'load', 'check_point',
               'check_point_time', 'active']

    order_columns = ['tracker', 'load', 'check_point',
               'check_point_time', 'active']
    max_display_length = 500

    def render_column(self, row, column):
        return super(TripListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(tracker_device_name__istartswith=search)
        return qs


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/accounts/login/')
def index(request):
    tracker_dict = {}
    context = {'devices': tracker_dict, 'mapbox_token': MAPBOX_ACCESS_TOKEN}
    return render(request, 'geo/index.html', context)

def trackers(request):
    tracker_dict = {}
    context = {'devices': tracker_dict}
    return render(request, 'geo/trackers.html', context)

def loads(request):
    context = {}
    return render(request, 'geo/loads.html', context)


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

def db(request):
    '''
    This is for creating stuff in db for testing
    :param request:
    :return:
    '''

    # List (Dict) of FencingModules currently along the highway, to be updated by Admin Only.
    # This would never actually show up in views, only stored through models.
    fencing_modules = {
        'WIFI-FencingMod1': ['Oak Park', 'IL', '60302', 41.881192, -87.777680],
        'FencingMod2': ['Alexandria', 'VA', '22314', 38.805336, -77.042894],
        'FencingMod3': ['Arlington', 'TX', '76011', 32.747115, -97.093164],
    }

    from faker import Faker
    fake = Faker()


    import pandas as pd

    import datetime

    created_date=datetime.date.today()

    #Clients
    cli, c = Client.objects.get_or_create(
        user = request.user
    )
    #Locations
    cities_df = pd.read_csv('cities.csv', sep='\t', lineterminator='\r')
    for i, city in cities_df.iterrows():
        print(city)
        city = i[1].strip()
        state = i[2].strip()
        zip = 22308#Faker.zip
        lat, lon = 40,40
        cit, c = Location.objects.get_or_create(
            city=city,
            state=state,
            zip=zip,
            lat=lat, lon=lon
        )
    #FencingModule

    for device_name, v in fencing_modules.items():
        loc = Location.objects.get(city='Chicago')
        fm, c = FencingModule.objects.get_or_create(
            device_name=device_name,
            created_date=created_date,
            loc=loc,
        )


    #TrackerChips

    url = "https://api.particle.io/v1/devices"

    payload = {}
    headers = {
        'Authorization': 'Bearer %s'%PARTICLE_ACCESS_TOKEN
    }

    devices_response = requests.request("GET", url, headers=headers, data=payload)
    for device_json in devices_response.json():

        print(device_json['name'], device_json)
        tc, c = TrackerChip.objects.get_or_create(
            device_name=device_json['name'],
            created_date=created_date,
            tracker_id=device_json['id'],
            # client=cli.pk
        )



    #Load
    #Trip

    fake.name()
    # 'Lucy Cechtelar'

    fake.address()

    return JsonResponse({"ok":"ok"})
