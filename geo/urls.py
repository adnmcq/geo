from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trackers', views.trackers, name='trackers'),
    path('loads', views.loads, name='loads'),


    #for testing
    path('api', views.api, name='api'),
    path('db', views.db, name='db'),
]