from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trackers', views.trackers, name='trackers'),
    path('loads', views.loads, name='loads'),


    url(r'^tracker/data/$', login_required(views.TrackerListJson.as_view()), name='tracker_list_json'),
    url(r'^load/data/$', login_required(views.LoadListJson.as_view()), name='load_list_json'),
    url(r'^trip/data/$', login_required(views.TripListJson.as_view()), name='trip_list_json'),

    path('add_trip_to_map', views.add_trip_to_map, name='add_trip_to_map'),

    #for testing
    path('api', views.api, name='api'),

]