from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/$', views.migrate_to_approval, name='migrate_to_approval'),
    # url(r'^api/all/(?P<pk>[0-9]+)$', views.get_all_approval_by_comp, name='get_all_approval_by_comp'),
    url(r'^api/all/(?P<pk>[0-9]+)', views.get_all_approval_by_comp, name='get_all_approval_by_comp'),
    url(r'^api/(?P<pk>[0-9]+)$', views.update_lookone_approval, name='update_lookone_approval'),
    # url(r'^api/user/(?P<pk>[0-9]+)$', views.get_post_certification_user, name='get_post_certification_user'),
]