from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)$', views.get_delete_update_registrations, name='get_delete_update_registrations'),
    url(r'^api/findfriends/(?P<pk>[0-9]+)$', views.get_user, name='get_user'),
    url(r'^api/$', views.get_post_registrations, name='get_post_registrations'),
    url(r'^api/upload/$', views.upload_xls, name='upload_xls'),
    url(r'^api/login/$', views.get_login, name='get_login'),
    url(r'^api/search/$', views.search, name='search'),
    # url(r'^api/confirm/$', views.verified_acc, name='verified_acc'),
    url(r'^api/forget/$', views.forget, name='forget'),
    url(r'^api/forgetbacklink/$', views.forget_backlink, name='forget_backlink'),
    url(r'^api/tes/$', views.attempt_login, name='attempt_login'),

    # new api for mindzzle
    url(r'^api/confirm/$', views.activate_email, name='activate_email'),
    url(r'^api/cek_login/$', views.cek_login_views, name='cek_login_views'),

    # api for crocodic
    url(r'^api/cek_token/$', views.login_token_views, name='login_token_views'),

]