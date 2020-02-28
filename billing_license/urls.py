from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/billing/$', views.billing_license_list, name='billing_license_list'),
]