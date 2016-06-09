
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^main/', views.main, name='main'),
    url(r'^generate/', views.generate_document, name='generate'),
    url(r'callback/', views.oauth_callback, name='callback'),
    url(r'code/', views.oauth_callback, name='code'),
    url(r'hook/', views.hook_callback, name='hook'),
    url(r'hook_create/', views.hook_creation_process, name='hook_create'),
    url(r'hook_int/', views.hook_test, name='hook_test'),
    url(r'hook_process/', views.hook_process, name='hook_process'),
    url(r'token_update/', views.token_save_process, name='token_update'),

]
