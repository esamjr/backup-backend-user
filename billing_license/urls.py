from django.conf.urls import url
from . import views

urlpatterns = [
    # license company
    url(r'^api/billing/$', views.billing_license_list, name='billing_license_list'),
    url(r'^api/update_date/$', views.update_license_date, name='update_license_date')


    # license user
]