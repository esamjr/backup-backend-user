from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/$', views.revies_sched, name='revies_sched'),
]
