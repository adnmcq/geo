from django.test import TestCase
import time
import urllib.request as urllib2
import json

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
