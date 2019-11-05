from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^apisuperadmin/$', views.auto_migrate_to_domoo, name='auto_migrate_to_domoo'),
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_registrations, name='get_delete_update_registrations'),
    url(r'^api/findFriends/(?P<pk>[0-9]+)$', views.get_user_by_email, name='get_user_by_email'),
    url(r'^api/$', views.get_post_registrations, name='get_post_registrations'),
    url(r'^api/upload/$', views.upload_xls, name='upload_xls'),
    url(r'^api/login/$', views.get_login, name='get_login'),
    url(r'^api/search/$', views.search, name='search'),
    url(r'^api/confirm/$', views.verified_acc, name='verified_acc'),
    url(r'^api/forget/$', views.forget, name='forget'),
    url(r'^api/forgetbacklink/$', views.forget_backlink, name='forget_backlink'),
    url(r'^api/tes/$', views.attempt_login, name='attempt_login'),
    url(r'^api/searchEmail/$', views.get_search_by_name, name='get_search_by_name'),
]