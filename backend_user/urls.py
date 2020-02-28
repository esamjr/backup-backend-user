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
from email_app import views as lihat

urlpatterns = [
    path('', include('pages.urls')),
    url(r'^orderlicense/', include('orderlicense.urls')),
    url(r'^warna/', include('warna_goal.urls')),
    url(r'^timeperiod/', include('time_period.urls')),
    url(r'^kpi/', include('KPI.urls')),
    url(r'^kpiassign/', include('KPI_assign.urls')),
    url(r'^kpi_category/', include('kpi_category.urls')),
    url(r'^task/', include('task.urls')),
    url(r'^taskchecklistitem/', include('task_checklist_item.urls')),
    url(r'^taskchecklisttemplate/', include('task_checklist_template.urls')),
    url(r'^tasktag/', include('task_tag.urls')),
    url(r'^taskcomment/', include('task_comment.urls')),
    url(r'^taskfollower/', include('task_follower.urls')),
    url(r'^taskassign/', include('task_assign.urls')),
    url(r'^tasktimer/', include('task_timer.urls')),
    url(r'^jobdesc/', include('jobdesc.urls')),
    url(r'^approval/', include('approval_config.urls')),
    url(r'^licensecomp/', include('license_company.urls')),
    url(r'^chatapp/', include('chatapp.urls')),
    url(r'^test/', include('test_form.urls')),
    url(r'^jobfair/', include('jobfair_online.urls')),
    url(r'^interview/', include('interview.urls')),
    url(r'^recruitment/', include('recruitment.urls')),
    url(r'^award_BA/', include('awards_BA.urls')),
    url(r'^certification_BA/', include('certifications_BA.urls')),
    url(r'^log_goal/', include('log_created_goal.urls')), 
    url(r'^goal_negotiation/', include('goal_negotiation.urls')), 
    url(r'^goal_assign/', include('goal_assignment.urls')), 
    url(r'^goal/', include('goal.urls')), 
    url(r'^review_scheduler/', include('review_scheduler.urls')),
    url(r'^type_goal/', include('type_goal.urls')), 
    url(r'^ocr/', include('OCR_Reader.urls')), 
    url(r'^uploadDOCuser/', include('user_img.urls')), 
    url(r'^uploadDOCcomp/', include('business_img.urls')), 
    url(r'^files/', include('file_upload.urls')), 
    url(r'^notfication/', include('notification.urls')), 
    url(r'^mailLog/', include('email_app.urls')), 
    url(r'^activitylog/', include('log_app.urls')), 
    url(r'^registrations/', include('registrations.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^business_account/', include('business_account.urls')),
    url(r'^user_type/', include('user_type.urls')),
    url(r'^friend_list/', include('friend_list.urls')),
    url(r'^country/', include('country.urls')),
    url(r'^region/', include('region.urls')),
    url(r'^city/', include('city.urls')),
    url(r'^vendor/', include('vendor_api.urls')),
    url(r'^experiences/', include('experiences.urls')),
    url(r'^education/', include('education.urls')),
    url(r'^award/', include('award.urls')),
    url(r'^certification/', include('certification.urls')),
    url(r'^join_company/', include('join_company.urls')),
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
    url(r'^private/', include('private.urls')),
    url(r'^goal_category/', include('goal_category.urls')),
    url(r'^goal_activity/', include('goal_activity.urls')),
    url(r'^goal_files/', include('goal_files.urls')),
    url(r'^goal_notes/', include('goal_notes.urls')),
    url(r'^goal_setting/', include('goal_setting.urls')),
    url(r'^goal_pinned/', include('goal_pinned.urls')),
    url(r'^tag/', include('tag.urls')),
    url(r'^milestone/', include('milestone.urls')),
    url(r'^feeds/', include('feeds.urls')),
    url(r'^friends/', include('friends.urls')),
    url(r'^group_user/', include('group_user.urls')),
    # url(r'^setting_approval/', include('setting_approval.urls')),
    url(r'^license_comp/', include('license_company.urls')),
    url(r'^billing_license/', include('billing_license.urls')),
]
