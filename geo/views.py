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


from django.views.decorators.csrf import csrf_exempt

# List (Dict) of FencingModules currently along the highway, to be updated by Admin Only.
# This would never actually show up in views, only stored through models.
fencing_modules = {
    'WIFI-FencingMod1': ['Oak Park', 'IL', '60302', 41.881192, -87.777680],
    'FencingMod2': ['Alexandria', 'VA', '22314', 38.805336, -77.042894],
    'FencingMod3': ['Arlington', 'TX', '76011', 32.747115, -97.093164],
}
from spyrk import SparkCloud

ACCESS_TOKEN = '170204c3da13da0fbb54f2ccd5301dcf209c56c5'

spark = SparkCloud(ACCESS_TOKEN)

tracker_dict = {}

for fm in fencing_modules:
    for s in spark.devices:
        if fm == s:
            tracker_dict[spark.devices[s].Name] = {"Time": spark.devices[s].Time, "CheckPoint_Name": fm, "CheckPoint_DeviceID": spark.devices[s].id, "CheckPoint_Location": fencing_modules[fm]}

print(tracker_dict)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/accounts/login/')
def index(request):
    context = {'devices': tracker_dict}
    return render(request, 'geo/index.html', context)

def trackers(request):
    context = {'devices': tracker_dict}
    return  render(request, 'geo/trackers.html', context)

