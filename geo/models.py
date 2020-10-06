from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from quiz.settings import MAPBOX_ACCESS_TOKEN, PARTICLE_ACCESS_TOKEN, MAPBOX_NO_LIMIT_ACCESS_TOKEN

import requests, datetime
import urllib.parse
import json

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username


class Location(models.Model):
    #https://docs.mapbox.com/api/search/#geocoding
    #use this to forward find the most populous 500 cities in the US
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=5, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    def __str__(self):
        return '(%s, %s) %s, %s %s'%(self.lat, self.lon, self.city, self.state, self.zip)

    def forward(self):
        '''
        Forward geocoding converts location text into geographic coordinates,
        turning 2 Lincoln Memorial Circle NW into -77.050,38.889.
        :return:
        '''

        search_string = urllib.parse.quote(self.city)#'Los%20Angeles'
        url = "https://api.mapbox.com/geocoding/v5/mapbox.places/%s.json?access_token=%s"%(search_string, MAPBOX_ACCESS_TOKEN)
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text.encode('utf8'))
        dict_str = response.text
        data = json.loads(dict_str)
        return data

    def reverse(self):
        '''
        Reverse geocoding turns geographic coordinates into place names, turning -77.050, 38.889 into 2 Lincoln Memorial Circle NW. These location names can vary in specificity,
        from individual addresses to states and countries that contain the given coordinates.
        :return:
        '''

        lat, lon = self.lat, self.lon
        url = "https://api.mapbox.com/geocoding/v5/mapbox.places/%s,%s.json?access_token=%s"%(lon, lat, MAPBOX_ACCESS_TOKEN)

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text.encode('utf8'))
        # text_response = response.text.encode('utf8')
        # return text_response
        dict_str = response.text
        data = json.loads(dict_str)
        return data

class FencingModule(models.Model): #Doesn't need any user auth since this will only be controlled by Admin
    '''
    These are the static 'central' scanners on the side of the highway.
    They do not move. All 'event' data comes from fencing module

    '''
    device_id = models.CharField(max_length=30, unique=True)
    device_name = models.CharField(max_length=40)
    created_date = models.DateTimeField(default= datetime.datetime.now())
    loc = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return '%s - %s'%(self.device_name, str(self.loc.city))

class TrackerChip(models.Model): #User auth required.  Users should only be able to see their specific trackers
    device_id = models.CharField(max_length=40, unique=True) #Unique ID labeled on the device - upload via qr code scanner
    device_name = models.CharField(max_length=40, unique=True)
    created_date = models.DateTimeField(default= datetime.datetime.now())
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return '%s - %s'%(self.device_id, self.device_name)


class Load(models.Model):
    REF_TYPES = (
        ('L', 'Load ID'),
        ('B', 'Bill of Lading'),
        ('P', 'PRO Number'),
        ('R', 'Purchase Order'),
        ('S', 'Sales Order'),
        ('O', 'Other'),
    )
    ref1_type = models.CharField(max_length=1, choices=REF_TYPES,null=True, blank=True)
    ref1 = models.CharField(max_length=20, null=True, blank=True)
    ref2_type = models.CharField(max_length=1, choices=REF_TYPES, null=True, blank=True)
    ref2 = models.CharField(max_length=20, null=True, blank=True)
    ref3_type = models.CharField(max_length=1, choices=REF_TYPES, null=True, blank=True)
    ref3 = models.CharField(max_length=20, null=True, blank=True)
    ref4_type = models.CharField(max_length=1, choices=REF_TYPES, null=True, blank=True)
    ref4 = models.CharField(max_length=20, null=True, blank=True)
    ref5_type = models.CharField(max_length=1, choices=REF_TYPES, null=True, blank=True)
    ref5 = models.CharField(max_length=20, null=True, blank=True)

    orig = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE, related_name='orig')
    dest = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE, related_name='dest')

    # tracker_chip = models.ForeignKey(TrackerChip, on_delete=models.CASCADE)
    tracker_chips = models.ManyToManyField(
        TrackerChip,
        through='Trip',
        through_fields=('load', 'tracker'),
    )

    def __str__(self):
        return 'orig: %s \ndest: %s'%(str(self.orig), str(self.dest))

    def directions(self):
        url = "https://api.mapbox.com/matching/v5/mapbox/driving?access_token=%s"%MAPBOX_ACCESS_TOKEN

        o, d = self.orig, self.dest

        '''
        payload = 'coordinates=-117.17282%2C32.71204%3B-117.17288%2C32.71225%3B-117.17293%2C32.71244%3B-117.17292%2C32.71256%3B-117.17298%2C32.712603%3B-117.17314%2C32.71259%3B-117.17334%2C32.71254'
        '''

        search_string = urllib.parse.quote("%s,%s;%s,%s"%(o.lon, o.lat, d.lon, d.lat))

        payload = 'coordinates=%s'%search_string
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text.encode('utf8'))
        dict_str = response.text
        data = json.loads(dict_str)
        return data

    def no_limit_directions(self):

        o, d = self.orig, self.dest


        search_string = urllib.parse.quote("%s,%s;%s,%s"%(o.lon, o.lat, d.lon, d.lat))

        #-118.243908%2C34.05487%3B-73.980715%2C40.764916

        #switch from geometries=polyline to geojson
        url = "https://api.mapbox.com/directions/v5/mapbox/driving/%s.json?geometries=geojson&alternatives=true&steps=true&overview=full&access_token=%s"%(search_string, MAPBOX_NO_LIMIT_ACCESS_TOKEN)

        # url = "https://api.mapbox.com/directions/v5/mapbox/driving/-118.243908%2C34.05487%3B-73.980715%2C40.764916.json?geometries=polyline&alternatives=true&steps=true&overview=full&access_token=pk.eyJ1IjoiZXhhbXBsZXMiLCJhIjoiY2p0MG01MXRqMW45cjQzb2R6b2ptc3J4MSJ9.zA2W0IkI0c6KaAhJfk9bWg"

        payload = {}
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Accept': '*/*',
            'Origin': 'https://docs.mapbox.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://docs.mapbox.com/',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        dict_str = response.text
        data = json.loads(dict_str)
        return data

class Trip(models.Model):
    tracker = models.ForeignKey(TrackerChip, on_delete=models.CASCADE)
    load = models.ForeignKey(Load, on_delete=models.CASCADE)

    check_point = models.ForeignKey(FencingModule, on_delete=models.CASCADE, null=True, blank=True)
    check_point_time = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return 'load: %s \ntracker: %s'%(self.load.id, str(self.tracker))