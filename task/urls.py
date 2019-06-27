from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'^api/$', views.get_post, name='get_post'),
   url(r'^api/(?P<pk>[0-9]+)$', views.get_put_delete, name='get_put_delete'),
   url(r'^reportperday/$', views.report_task_perday, name='report_task_perday'),
]
