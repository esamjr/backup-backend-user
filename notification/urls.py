from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^api/(?P<pk>[0-9]+)$', views.notification_user, name='notification_user'),    
    url(r'^api/fcm/$', views.notifications_fcm, name='notifications_fcm'),
]
