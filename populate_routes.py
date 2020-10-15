
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
with concurrent.futures.ThreadPoolExecutor() as executor:
    pass
executor.shutdown(wait=True)

def get_querysets(qset):
    return len(qset)

#from https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Threading/threading-demo.py
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     start_time = time.time()
#     # qsets = [all_rts, city2city_rts, city2pilot_rts,
#     #       pilot2city_rts, pilot2pilot_rts]  #TODO UNDO
#     qsets = [city2city_rts]
#     results = executor.map(get_querysets, qsets)  #starts and joins threads
#     for result in results:
#         # print(result)
#         pass
#     print("--- %s seconds to get qsets w threading ---" % (time.time() - start_time))
#     pt="--- %s seconds to get qsets w threading ---" % (time.time() - start_time)
#     logger.info(pt)
#
# executor.shutdown(wait=True)

# city2city_rts = Route.objects.filter(orig__in=city_locs, dest__in=city_locs)


#for testing just N Ill and WI
routes_to_set = Route.objects.all()


def loop_thru_routes(routes = []):
    for rt in routes:
        rt.no_limit_directions(test=1)
    return 1

# start_time = time.time()
# loop_thru_routes()
# print("--- %s seconds LOOP NO threading ---" % (time.time() - start_time))  #141.46203207969666 seconds LOOP NO threading
# pt = "--- %s seconds LOOP NO threading ---" % (time.time() - start_time)
# logger.info(pt)


def chunks(lst, chunk_size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


ndoneqs = routes_to_set.filter(route={})
# if not ndoneqs.exists():
    # break  # they've all been done

chunk_size = int(len(ndoneqs)/5)
not_done_query_sets = list(chunks(ndoneqs, chunk_size))

for ii, sub_qs in enumerate(not_done_query_sets):


    print ('Iteration', ii)
    ndone = len(ndoneqs)

    # print(ndone)
    logger.info(ndone)


    divsors = [1]#aka num of threads  - I think 2 threads now gives me a 429 response on API request
    for div in divsors:
        with concurrent.futures.ThreadPoolExecutor() as executor:

            chunk_size = int(len(sub_qs)/div)

            start_time = time.time()


            thread_sets = list(chunks(sub_qs, chunk_size))  #not how many chunks, but chunks of this size
            results = executor.map(loop_thru_routes, thread_sets)  # starts and joins threads
            for _ in results:
                pass

            pt = "--- %s seconds LOOP w %s threads for %s obj ---" % (time.time() - start_time, div, len(sub_qs))

            print(pt)  #--- 122.60925316810608 seconds LOOP w threading ---  5threads, no real work per loop
            logger.info(pt)

        executor.shutdown(wait=True)





#https://stackoverflow.com/questions/2632520/what-is-the-fastest-way-to-send-100-000-http-requests-in-python



    #https://docs.python.org/3/library/concurrent.futures.html
    # with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    #     things_to_work = (executor.submit(load_url, url, TIMEOUT) for url in urls)
    #     time1 = time.time()
    #     for future in concurrent.futures.as_completed(things_to_work):
    #         try:
    #             data = future.result()
    #         except Exception as exc:
    #             data = str(type(exc))
    #         finally:
    #             out.append(data)
    #
    #             print(str(len(out)),end="\r")
    #
    #     time2 = time.time()

    # print(f'Took {time2-time1:.2f} s')


