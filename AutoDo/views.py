__author__ = 'user'

from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms

def index(request):
    return render_to_response('index.html', {}, RequestContext(request))


def token(request):
    token = request.GET['access_token']
    return render_to_response('index.html', {}, RequestContext(request))
