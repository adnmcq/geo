
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


#django querysets only calculated if used later in the code (I think)
city_locs = all_locs[:316]
all_rts = Route.objects.all()
city2city_rts = Route.objects.filter(orig__in=city_locs, dest__in=city_locs)
city2pilot_rts = Route.objects.filter(orig__in=city_locs).exclude(dest__in=city_locs)
pilot2city_rts = Route.objects.filter(dest__in=city_locs).exclude(orig__in=city_locs)
pilot2pilot_rts = Route.objects.all().exclude(orig__in=city_locs).exclude(dest__in=city_locs)
#
# def get_qs_no_thread():
#     nums = [len(all_rts), len(city2city_rts), len(city2pilot_rts),
#           len(pilot2city_rts), len(pilot2pilot_rts)]
#     print(nums)
#
#     print(['{0:.3g}'.format(num/3600.) for num in nums])
#
# # get_qs_no_thread()


'''
all      c2c   c2p    p2c    p2p
1248000 99856 253432 253112 641600
seconds to hours
346.67 27.738 70.3978 70.3089 178.23
'''
import multiprocessing, threading, concurrent

def get_querysets(qset):
    return len(qset)

#from https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Threading/threading-demo.py
with concurrent.futures.ThreadPoolExecutor() as executor:
    start_time = time.time()
    # qsets = [all_rts, city2city_rts, city2pilot_rts,
    #       pilot2city_rts, pilot2pilot_rts]  #TODO UNDO
    qsets = [city2city_rts]
    results = executor.map(get_querysets, qsets)  #starts and joins threads
    for result in results:
        print(result)

    print("--- %s seconds to get qsets w threading ---" % (time.time() - start_time))
    pt="--- %s seconds to get qsets w threading ---" % (time.time() - start_time)
    logger.info(pt)



def loop_thru_routes(routes = city2city_rts):
    for rt in routes:
        city = rt.orig.city
    return 1

start_time = time.time()
loop_thru_routes()
print("--- %s seconds LOOP NO threading ---" % (time.time() - start_time))  #141.46203207969666 seconds LOOP NO threading
pt = "--- %s seconds LOOP NO threading ---" % (time.time() - start_time)
logger.info(pt)


def chunks(lst, chunk_size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

with concurrent.futures.ThreadPoolExecutor() as executor:
    divsors = [1, 10, 100, 1000, 10000]#aka num of threads
    for div in divsors:

        chunk_size = int(len(city2city_rts)/div)
        start_time = time.time()
        # div = int(len(city2city_rts)/5)
        # print(type(div))
        # qsets = [city2city_rts[:div], city2city_rts[div:2*div], city2city_rts[2*div:3*div],
        #          city2city_rts[3*div:4*div], city2city_rts[4*div:]]

        qsets = list(chunks(city2city_rts, chunk_size))  #not how many chunks, but chunks of this size
        results = executor.map(loop_thru_routes, qsets)  # starts and joins threads
        for result in results:
            # print(result)
            pass

        pt = "--- %s seconds LOOP w %s threads ---" % (time.time() - start_time, div)

        print(pt)  #--- 122.60925316810608 seconds LOOP w threading ---  5threads, no real work per loop
        logger.info(pt)



    #125 seconds 99856/500 (200)  threads

    #  seconds 99856/50  (2000) threads

    #  134 seconds 99856/5  (20k) threads




#https://stackoverflow.com/questions/2632520/what-is-the-fastest-way-to-send-100-000-http-requests-in-python


import pandas as pd
import concurrent.futures
import requests
import time


def conc():
    out = []
    CONNECTIONS = 100
    TIMEOUT = 5

    tlds = open('../data/sample_1k.txt').read().splitlines()
    urls = ['http://{}'.format(x) for x in tlds[1:]]

    def load_url(url, timeout):
        ans = requests.head(url, timeout=timeout)
        return ans.status_code

    #https://docs.python.org/3/library/concurrent.futures.html
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
        time1 = time.time()
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                out.append(data)

                print(str(len(out)),end="\r")

        time2 = time.time()

    print(f'Took {time2-time1:.2f} s')
    print(pd.Series(out).value_counts())

