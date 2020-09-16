from django.db import models

class FencingModule(models.Model): #Doesn't need any user auth since this will only be controlled by Admin
    device_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    created_date = models.DateTimeField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

class TrackerChip(models.Model): #User auth required.  Users should only be able to see their specific trackers
    tracker_id = models.CharField(max_length=12) #Unique ID labeled on the device - upload via qr code scanner
    device_name = models.CharField(max_length=30)
    created_date = models.DateTimeField()

class Load(models.Model):
    REF_TYPES = (
        ('L', 'Load ID'),
        ('B', 'Bill of Lading'),
        ('P', 'PRO Number'),
        ('R', 'Purchase Order'),
        ('S', 'Sales Order'),
    )
    ref1_type = models.CharField(max_length=1, choices=REF_TYPES)
    ref1 = models.CharField(max_length=20)
    ref2_type = models.CharField(max_length=1, choices=REF_TYPES)
    ref2 = models.CharField(max_length=20)
    ref3_type = models.CharField(max_length=1, choices=REF_TYPES)
    ref3 = models.CharField(max_length=20)
    ref4_type = models.CharField(max_length=1, choices=REF_TYPES)
    ref4 = models.CharField(max_length=20)
    ref5_type = models.CharField(max_length=1, choices=REF_TYPES)
    ref5 = models.CharField(max_length=20)
    tracker_chip = models.ForeignKey(TrackerChip)
    #orign =
    #dest =

class Trip(models.Model):
    load = models.ForeignKey(Load)
    check_point = models.ForeignKey(FencingModule)
    check_point_time = models.DateTimeField()

