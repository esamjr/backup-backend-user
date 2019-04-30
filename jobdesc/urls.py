from django.conf.urls import url
from . import views

urlpatterns = [   
    url(r'^api/(?P<pk>[0-9]+)$', views.automigrate_hierarchy_to_jobdesc, name='automigrate_hierarchy_to_jobdesc'),    
]