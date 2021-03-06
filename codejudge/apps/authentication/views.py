#!/usr/bin/python

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sessions.models import Session
from django.conf import settings
from django.conf.urls.static import static
from apps.judge.models import *
from datetime import *
import json
import requests
import commands, unicodedata
import random, string, os, subprocess
from django.utils import timezone

def userLogin(request):
    try:
        if request.session['username']:
            return HttpResponseRedirect("/judge")
    except KeyError:
        context = RequestContext(request)
        error = False
        if request.method == 'POST' and request.is_ajax():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user != None:
                if user.is_authenticated():
                    login(request, user)
                    request.session['username']  = username
                    request.session['password']  = password
                    return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
                else:
                    error = True
                    return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
            else:
                error = True
                return HttpResponse(json.dumps({'errors': error}),content_type='application/json')

        return render(request, 'users/login.html')

@login_required
def userLogout(request):
    del request.session['username']
    del request.session['password'] 
    logout(request)
    return HttpResponseRedirect("/judge")

@login_required
def changePassword(request):
    error = 0
    if request.method == "POST":
        old_password = request.POST['oldPassword']
        new_password = request.POST['newPassword']
        user = authenticate(username=request.session['username'], password=old_password)
        if user is not None:
            query = Hacker.objects.get(username=request.session['username'])
            query.set_password(new_password)
            query.save()
            error = 1
            return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
        else:
            error = 2
            return HttpResponse(json.dumps({'errors': error}),content_type='application/json')

def newUser(request):
    return render(request, 'users/register.html')

@login_required
def userLogout(request):
    del request.session['username']
    del request.session['password'] 
    logout(request)
    return HttpResponseRedirect("/judge")

@login_required
def profile(request):
    hacker = Hacker.objects.get(username = request.session['username'])
    return render(request, 'users/profile.html', {'hacker':hacker})  

@login_required
def editProfile(request):
    h = Hacker.objects.get(username=request.session['username'])
    return render(request, 'users/edit_profile.html', {'hacker':h})

@login_required
def editUser(request):
    h = Hacker.objects.get(username=request.session['username'])
    error = 0
    h.first_name = request.POST['newFirstName']
    h.last_name = request.POST['newLastName']
    h.save()
    return HttpResponse(json.dumps({'errors': error}),content_type='application/json')

@login_required
def change(request):
    return render(request, 'users/changepass.html')

def register(request): 
    errors = False
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['user_name']
        password = request.POST['pass_word']
        email = request.POST['email']
        roll = str(request.POST['roll'])
        query = Hacker.objects.filter(username=username)
        if query:
            errors = True
        else:
            user = Hacker.objects.create_user(username, email, password)
            user.roll = roll
            user.save()
            payload = {'username':username,'password':password,'email':email}
            requests.get("http://localhost:8000/v1/userRegister",params=payload)
            user = authenticate(username=username, password=password)
            login(request, user)
            
            request.session['username']  = username
            request.session['password']  = password
            
        return HttpResponse(json.dumps({'errors': errors}),content_type='application/json')
    else:
        raise Http404

def handler404(request):
    response = render_to_response('user/login.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response