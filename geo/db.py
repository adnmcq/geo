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
import platform

def db():
    '''
    This is for creating stuff in db for testing
    :param request:
    :return:
    '''

    Route.objects.all().delete()

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

    #add truckstop locations
    '''
    Store#,Name,Address,City,State/Province,Country,Zip,Interstate,Latitude,Longitude,Phone,Fax,Parking Spaces,Diesel Lanes,Bulk DEF Lanes,Showers,CAT Scale,Facilities/Restaurants,WiFi
1,"Pilot Travel Center","5868 Nittany Valley Drive","Mill Hall","PA","US","17751","I-80  Exit 173","41.03395900","-77.51567200","(570) 726-7618","(570) 726-5092","70","8","8","5","Yes","Subway, Breakfast/Soup Bar, Cinnabon","No",

    '''
    fencing_df = pd.read_csv(os.path.join(BASE_DIR, 'pilot_locations.csv'))
    for i, r in fencing_df.iterrows():

        #oboe bc uses the store # as ID
        ts, c = Location.objects.get_or_create(
            city=r[2],
            state=r[3],
            zip=None,
            lat=r[7], lon=r[8]
        )




    #FencingModule

    url = "https://api.particle.io/v1/devices"

    payload = {}
    headers = {
        'Authorization': 'Bearer %s'%PARTICLE_ACCESS_TOKEN
    }

    devices_response = requests.request("GET", url, headers=headers, data=payload)
    for device_json in devices_response.json():

        print(device_json)
        if 'Fencing'  in device_json['name']:
            city_name = device_json['name'].split('_')[1]
            loc = Location.objects.filter(city=city_name)[0]
            fm, c = FencingModule.objects.get_or_create(
                device_name=device_json['name'],
                #created_date=created_date,
                device_id=device_json['id'],
                loc=loc
            )



    #Fake Tracker
    tc, c = TrackerChip.objects.get_or_create(
        device_name='TIM69_420',
        #created_date=created_date,
        device_id='abdc',
        client=cli
        )

    # CREATE SOME FAKE LOADS
    origins = ['Temecula','Pueblo','Topeka']
    destinations = ['Abilene','Simi Valley','Fargo']


    for o, d in zip(origins, destinations):
        oo = Location.objects.filter(city = o)[0]
        do = Location.objects.filter(city = d)[0]

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




if 0:#platform.system() == 'Windows':
    route_locs = Location.objects.all()
    bulk_chunk = 6000
else:
    route_locs = Location.objects.filter(lat__lt=43, lat__gt=41,

                                         lon__lt=-87, lon__gt=-90,)

    print('# NIL LOCS %s'%len(route_locs))
    bulk_chunk = 200

def make_empty_routes():
    # all_locs = Location.objects.all()
    i=0
    Route.objects.all().delete()
    entries = []
    for o in route_locs:
        for d in route_locs:
            i+=1
            entries.append(Route(orig=o, dest=d))
            if i%bulk_chunk==0 or i==len(route_locs)**2:
                print(i)
                Route.objects.bulk_create(entries)

                entries = []



    print('# Routes NIL WI',len(Route.objects.all()))

make_empty_routes()