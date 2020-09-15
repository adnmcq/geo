from django.contrib import admin

from .models import *

admin.site.register([Quiz, Round, Question, Player, Team, Game])