from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/$', views.open_log, name='open_log'),
]
