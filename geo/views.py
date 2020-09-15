# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import *
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout, authenticate

from django.urls import reverse


from django.db.utils import IntegrityError


from .forms import *
import json
import math
import random
import html


from django.views.decorators.csrf import csrf_exempt

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='/accounts/login/')
def index(request):
    context = {}
    return render(request, 'quizapp/index.html', context)

