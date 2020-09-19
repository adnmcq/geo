from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

import requests


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

class FencingModule(models.Model): #Doesn't need any user auth since this will only be controlled by Admin
    '''
    These are the static 'central' scanners on the side of the highway. They do not move

    '''
    device_name = models.CharField(max_length=30)
    created_date = models.DateTimeField()
    loc = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
    # city = models.CharField(max_length=30)
    # state = models.CharField(max_length=2)
    # zip_code = models.CharField(max_length=5)
    # lat = models.DecimalField(max_digits=9, decimal_places=6)
    # lon = models.DecimalField(max_digits=9, decimal_places=6)
    def __str__(self):
        return '%s - %s'%(self.device_name, str(self.loc))

class TrackerChip(models.Model): #User auth required.  Users should only be able to see their specific trackers
    tracker_id = models.CharField(max_length=12, null=True, blank=True) #Unique ID labeled on the device - upload via qr code scanner
    device_name = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateTimeField()
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return '%s - %s'%(self.tracker_id, self.device_name)


class Load(models.Model):
    REF_TYPES = (
        ('L', 'Load ID'),
        ('B', 'Bill of Lading'),
        ('P', 'PRO Number'),
        ('R', 'Purchase Order'),
        ('S', 'Sales Order'),
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

# class Trip(models.Model):
#     load = models.ForeignKey(Load, on_delete=models.CASCADE)
#     check_point = models.ForeignKey(FencingModule, on_delete=models.CASCADE)
#     check_point_time = models.DateTimeField()


class Trip(models.Model):
    tracker = models.ForeignKey(TrackerChip, on_delete=models.CASCADE)
    load = models.ForeignKey(Load, on_delete=models.CASCADE)

    check_point = models.ForeignKey(FencingModule, on_delete=models.CASCADE, null=True, blank=True)
    check_point_time = models.DateTimeField(null=True, blank=True)

    active = models.NullBooleanField()

    def __str__(self):
        return 'load: %s \ntracker: %s'%(self.load.id, str(self.tracker))