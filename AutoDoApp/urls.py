__author__ = 'user'

from django.conf.urls import *

urlpatterns = [
    url(r'(?P<band_id>\d+)/$', 'AutoDoApp.views.band'),
]
