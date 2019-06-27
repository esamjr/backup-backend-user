from django.conf.urls import url
from . import views


urlpatterns = [

    # url(r'^api/(?P<pk>[0-9]+)$', # urls with details i.e /movies/(1-9)
    #     views.get_delete_update_movie,
    #     name='get_delete_update_movie'
    # ),
    url(
        r'^api/$', # urls list all and create new one)
        views.pilih_sku,
        name='pilih_sku'
    ),
    # url(
    #     r'^api/$', # urls list all and create new one
    #     views.get_post_movies,
    #     name='get_post_movies'
    # )
]