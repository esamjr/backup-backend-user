"""backend_user URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from registrations import views as lihat

urlpatterns = [
    
    url(r'^registrations/', include('registrations.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^business_account/', include('business_account.urls')),
    url(r'^user_type/', include('user_type.urls')),
    url(r'^friend_list/', include('friend_list.urls')),
    url(r'^country/', include('country.urls')),
    url(r'^region/', include('region.urls')),
    url(r'^city/', include('city.urls')),
    url(r'^message/', include('message.urls')),
    url(r'^experiences/', include('experiences.urls')),
    url(r'^education/', include('education.urls')),
    url(r'^award/', include('award.urls')),
    url(r'^certification/', include('certification.urls')),
    url(r'^join_company/', include('join_company.urls')),
    url(r'^business_account/', include('business_account.urls')),
    url(r'^business_type/', include('business_type.urls')),
    url(r'^employee_sign/', include('employee_sign.urls')),
    url(r'^history_hierarchy/', include('history_hierarchy.urls')),
    url(r'^hierarchy/', include('hierarchy.urls')),
    url(r'^contract/', include('contract.urls')),
    url(r'^job_contract/', include('job_contract.urls')),
    url(r'^level/', include('level.urls')),
    url(r'^time_contract/', include('time_contract.urls')),
    url(r'^type_time/', include('type_time.urls')),
    url(r'^role_type/', include('role_type.urls')),
]
