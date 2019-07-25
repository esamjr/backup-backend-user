from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.setting_license_company, name='setting_license_company'),
    # url(r'^api/filter/(?P<pk>[0-9]+)$', views.get_all_historyhierarchy, name='get_all_historyhierarchy'),
    url(r'^api/$', views.search_all_div, name='search_all_div'),
    url(r'^api/period/$', views.reminder_exp_date, name='reminder_exp_date'),
]
