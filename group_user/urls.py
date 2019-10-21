from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.setting_groups, name='setting_groups'),
    # url(r'^api/filter/(?P<pk>[0-9]+)$', views.get_all_historyhierarchy, name='get_all_historyhierarchy'),
    url(r'^api/$', views.search_all_div, name='search_all_div'),
]
