from django.db import models


class Business(models.Model):
    id_user = models.IntegerField()    
    company_name = models.CharField(max_length=255)
    email = models.CharField (max_length=255, unique=True, null = True, blank=True)
    primary_phone = models.CharField(max_length = 20, null = True, blank=True)
    primary_address = models.CharField(max_length=255, null = True, blank=True)
    id_country = models.IntegerField(null=True, blank=True)
    id_regions = models.IntegerField(null=True, blank=True)
    id_city = models.IntegerField(null=True, blank=True)
    id_business_type = models.IntegerField(null=True, blank=True)
    tax_num = models.IntegerField(null=True, blank=True)
    logo_path = models.TextField(default = 'http://dev-user-admin.mindzzle.com/static/img/blank_business.503c6c8.jpg',blank = True, null=True)
    description = models.TextField(blank=True, null = True)
    banned_type = models.CharField(max_length=500, blank = True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(auto_now=True)
    parent_company = models.IntegerField(blank = True, null=True, default = 0)
