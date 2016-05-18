
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'callback/', views.oauth_callback, name='callback'),
    url(r'code/', views.oauth_callback, name='code'),
    url(r'hook/', views.hook_callback, name='hook'),
    url(r'^(?P<access_token>[\w\-]+)/$', views.index, name='index'),
]
