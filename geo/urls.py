from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # path('2', views.index, name='index'),
    # path('add_trip_to_map', views.add_trip_to_map, name='add_trip_to_map'),
    # path('trackers', views.trackers, name='trackers'),   #show all trackers
    # path('loads', views.loads, name='loads'),    #show all trackers

    path('tracker/<int:d_id>', views.tracker, name='tracker'),  # add/ update trackers
    path('tracker', views.tracker, name='tracker'),  # add/ update trackers


    path('trip/<int:d_id>', views.trip, name='trip'),  # add/ update trips
    path('trip', views.trip, name='trip'),  # add/ update trips


    path('events/<str:device_id>', views.events, name='event'),  #Webhook endpoint


    url(r'^tracker/data/$', login_required(views.TrackerListJson.as_view()), name='tracker_list_json'),
    # url(r'^load/data/$', login_required(views.LoadListJson.as_view()), name='load_list_json'),
    url(r'^trip/data/$', login_required(views.TripListJson.as_view()), name='trip_list_json'),




    #OPTIMIZE?
    path('', views.index2, name='index'),
    path('add_trip_to_map2', views.add_trip_to_map2, name='add_trip_to_map2'),

    #add_fencing
    path('add_fencing', views.add_fencing, name='add_fencing'),


]