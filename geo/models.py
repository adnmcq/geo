from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from quiz.settings import MAPBOX_ACCESS_TOKEN, PARTICLE_ACCESS_TOKEN

import requests, datetime
import urllib.parse


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
        text_response = response.text.encode('utf8')
        return text_response

    def reverse(self):
        '''
        Reverse geocoding turns geographic coordinates into place names, turning -77.050, 38.889 into 2 Lincoln Memorial Circle NW. These location names can vary in specificity,
        from individual addresses to states and countries that contain the given coordinates.
        :return:
        '''

        lat, lon = -73.989,40.733
        url = "https://api.mapbox.com/geocoding/v5/mapbox.places/%s,%s.json?access_token=%s"%(lat, lon, MAPBOX_ACCESS_TOKEN)

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text.encode('utf8'))
        text_response = response.text.encode('utf8')
        return text_response

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
        return '%s - %s'%(self.device_name, str(self.loc))

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

class Trip(models.Model):
    tracker = models.ForeignKey(TrackerChip, on_delete=models.CASCADE)
    load = models.ForeignKey(Load, on_delete=models.CASCADE)

    check_point = models.ForeignKey(FencingModule, on_delete=models.CASCADE, null=True, blank=True)
    check_point_time = models.DateTimeField(null=True, blank=True)

    active = models.NullBooleanField()

    def __str__(self):
        return 'load: %s \ntracker: %s'%(self.load.id, str(self.tracker))