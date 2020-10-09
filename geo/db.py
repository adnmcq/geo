import os, platform

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

def db():
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

    if platform.system() == 'Windows':
        lt = '\r'
    else:
        lt = '\n'
    cities_df = pd.read_csv(os.path.join(base_dir, 'cities.csv'),
                            sep='\t', lineterminator=lt)

    print(cities_df)
    for i, city_row in cities_df.iterrows():
        print(city_row)
        city = i[1].strip()
        state = i[2].strip()
        zipc = None#Faker.zip
        location_string = city_row['Location']
        parts = location_string.split(' ')
        lat, lon = re.findall( r'\d+\.*\d*', parts[0])[0], \
                   re.findall( r'\d+\.*\d*', parts[1])[0]

        lat, lon = float(lat), -1*float(lon)
        cit, c = Location.objects.get_or_create(
            city=city,
            state=state,
            zip=zipc,
            lat=lat, lon=lon
        )

        # extra = cit.forward()
        # extra2 = cit.reverse()


    #FencingModule

    url = "https://api.particle.io/v1/devices"

    payload = {}
    headers = {
        'Authorization': 'Bearer %s'%PARTICLE_ACCESS_TOKEN
    }

    devices_response = requests.request("GET", url, headers=headers, data=payload)
    for device_json in devices_response.json():

        print(device_json)
        if 'Fencing' not in device_json['name']:
            #I don't think this hits, i think all 'devices' are FencingModules
            tc, c = TrackerChip.objects.get_or_create(
                device_name=device_json['name'],
                #created_date=created_date,
                device_id=device_json['id'],
                client=cli
            )
        else:
            city_name = device_json['name'].split('_')[1]
            loc = Location.objects.get(city=city_name)
            fm, c = FencingModule.objects.get_or_create(
                device_name=device_json['name'],
                #created_date=created_date,
                device_id=device_json['id'],
                loc=loc
            )

    #Load
    origins = ['Temecula','Pueblo','Topeka']
    destinations = ['Abilene','Simi Valley','Fargo']

    #CREATE SOME FAKE LOADS

    for o, d in zip(origins, destinations):
        oo = Location.objects.get(city = o)
        do = Location.objects.get(city = d)

        fm, c = Load.objects.get_or_create(
            ref1_type='L',
            ref1=o[0:3]+d[0:3],
            orig=oo, dest=do, client=cli
        )
        #THIS NEXT PART IS DONE IN WEBHOOK
        # if c:
        #     fm.tracker_chips.add(tracker)

    return 'ok'


db()