import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz.settings")

import django
django.setup()

from django.conf import settings
base_dir = settings.BASE_DIR

from geo.models import *
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(base_dir, 'conf.ini'))
MAPBOX_ACCESS_TOKEN = config['TOKENS']['mapbox'] if not os.environ.get('MAPBOX_ACCESS_TOKEN') else os.environ.get('MAPBOX_ACCESS_TOKEN')
PARTICLE_ACCESS_TOKEN = config['TOKENS']['particle'] if not os.environ.get('PARTICLE_ACCESS_TOKEN') else os.environ.get('PARTICLE_ACCESS_TOKEN')

from faker import Faker

fake = Faker()

import pandas as pd
import re

import datetime

created_date=datetime.date.today()

def a():
    '''
    This is for creating stuff in db for testing
    :param request:
    :return:
    '''

    Trip.objects.all().delete()
    Load.objects.all().delete()
    TrackerChip.objects.all().delete()
    FencingModule.objects.all().delete()
    Location.objects.all().delete()

    # List (Dict) of FencingModules currently along the highway, to be updated by Admin Only.
    # This would never actually show up in views, only stored through models.
    fencing_modules = {
        'WIFI-FencingMod1': ['Oak Park', 'IL', '60302', 41.881192, -87.777680],
        'FencingMod2': ['Alexandria', 'VA', '22314', 38.805336, -77.042894],
        'FencingMod3': ['Arlington', 'TX', '76011', 32.747115, -97.093164],
    }





    #Clients
    cli, c = Client.objects.get_or_create(
        user = User.objects.get(username='ksalette')
    )
    #Locations
    print('Location')
    cities_df = pd.read_csv(os.path.join(base_dir, 'cities.csv'),
                            sep='\t', lineterminator='\r')

    print(cities_df)
    for i, city_row in cities_df.iterrows():
        print(city_row)
        city = i[1].strip()
        state = i[2].strip()
        zipc = 22308#Faker.zip
        location_string = city_row['Location']
        parts = location_string.split(' ')
        lat, lon = re.findall( r'\d+\.*\d*', parts[0])[0], \
                   re.findall( r'\d+\.*\d*', parts[1])[0]
        cit, c = Location.objects.get_or_create(
            city=city,
            state=state,
            zip=zipc,
            lat=lat, lon=lon
        )

    # sid = transaction.savepoint()
    # transaction.savepoint_commit(sid)
    # qs = Location.objects.all()
    # for item in qs:
    #     item.save()
    # qs = TrackerChip.objects.all()
    # for item in qs:
    #     item.save()
    #FencingModule
    #TrackerChips


def b():

    cli= Client.objects.get(
        user = User.objects.get(username='ksalette')
    )

    url = "https://api.particle.io/v1/devices"

    payload = {}
    headers = {
        'Authorization': 'Bearer %s'%PARTICLE_ACCESS_TOKEN
    }

    devices_response = requests.request("GET", url, headers=headers, data=payload)
    for device_json in devices_response.json():

        print(device_json)
        if 'Fencing' not in device_json['name']:
            tc, c = TrackerChip.objects.get_or_create(
                device_name=device_json['name'],
                created_date=created_date,
                tracker_id=device_json['id'],
                client=cli
            )
        else:
            loc = Location.objects.get(city='Chicago')
            fm, c = FencingModule.objects.get_or_create(
                device_name=device_json['name'],
                created_date=created_date,
                loc=loc,
            )

    # sid2 = transaction.savepoint()
    # transaction.savepoint_commit(sid2)

    #Load
    origins = ['Temecula','Pueblo','Topeka']
    destinations = ['Abilene','Simi Valley','Fargo']

    tracker = TrackerChip.objects.get(device_name= 'LTE-BeaconFinder1')
    for o, d in zip(origins, destinations):
        oo = Location.objects.get(city = o)
        do = Location.objects.get(city = d)

        fm, c = Load.objects.get_or_create(
            ref1_type='L',
            ref1=o[0:3]+d[0:3],
            orig=oo, dest=do,


        )
        if c:
            fm.tracker_chips.add(tracker)

    #Trip

    fake.name()
    # 'Lucy Cechtelar'

    fake.address()

    return 'ok'


a()

b()