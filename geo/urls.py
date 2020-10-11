from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [

    #ModelForm for Tracker
    path('tracker/<int:d_id>', views.tracker, name='tracker'),  # add/ update trackers
    path('tracker', views.tracker, name='tracker'),  # add/ update trackers


    path('edit_trip/<int:d_id>', views.edit_trip, name='edit_trip'),  # update trip TODO
    path('add_trip', views.add_trip, name='add_trip'),  # add trip form (NOT a modelform)


    path('events/<str:device_id>', views.events, name='event'),  #Webhook endpoint


    url(r'^tracker/data/$', login_required(views.TrackerListJson.as_view()), name='tracker_list_json'),
    # url(r'^load/data/$', login_required(views.LoadListJson.as_view()), name='load_list_json'),
    url(r'^trip/data/$', login_required(views.TripListJson.as_view()), name='trip_list_json'),




    #OPTIMIZE?
    path('', views.index, name='index'),
    path('add_trip_to_map', views.add_trip_to_map, name='add_trip_to_map'),

    path('add_fencing', views.add_fencing, name='add_fencing'),
    path('loc_autocomplete', views.loc_autocomplete, name='loc_autocomplete'),

    #Keith wants separate link/pages for managing trackers and trips
    path('manage_trackers', views.manage_trackers, name='manage_trackers'),
    path('manage_trips', views.manage_trips, name='manage_trips'),


]