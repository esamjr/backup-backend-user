from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_jobcontract, name='get_delete_update_jobcontract'),
    url(r'^api/filter/(?P<pk1>[0-9]+)$', views.get_all_jobcontract, name='get_all_jobcontract'),
    # url(r'^api/$', views.get_post_jobcontract, name='get_post_jobcontract'),

    # new api for handle asign job
    url(r'^api/$', views.job_contract_views, name='job_contract_views'),
]
