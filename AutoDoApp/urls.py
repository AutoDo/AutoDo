
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'callback/', views.oauth_callback, name='callback'),
    url(r'^(?P<access_token>[\w\-]+)/$', views.index, name='index'),


]
