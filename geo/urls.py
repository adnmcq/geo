from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('quizzes', views.quizzes, name='quizzes'),
    # path('leaderboard', views.leaderboard, name='leaderboard'),
]