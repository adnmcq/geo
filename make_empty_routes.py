
import os, platform

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz.settings")

import time

import django
django.setup()

from django.conf import settings
base_dir = settings.BASE_DIR


from geo.models import *
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(base_dir, 'conf.ini'))

from quiz.settings import MAPBOX_ACCESS_TOKEN, PARTICLE_ACCESS_TOKEN, MAPBOX_NO_LIMIT_ACCESS_TOKEN

import pandas as pd
import re

import datetime

# print(MAPBOX_NO_LIMIT_ACCESS_TOKEN)

all_locs = Location.objects.all()

def make_empty_routes():
    # all_locs = Location.objects.all()
    i=0
    Route.objects.all().delete()
    entries = []
    for o in all_locs:
        for d in all_locs:
            i+=1
            entries.append(Route(orig=o, dest=d))
            if i%6000==0:
                print(i)
                Route.objects.bulk_create(entries)

                entries = []
            # r, c = Route.objects.get_or_create(orig=o, dest=d)

    print(i)

make_empty_routes()
# Route.objects.all().delete()