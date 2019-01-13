from django.db import models

class Business(models.Model):
    id_user = models.IntegerField()
    company_name = models.CharField(max_length=255)
    email = models.CharField (max_length=255, unique=True)
    primary_phone = models.IntegerField()
    primary_address = models.CharField(max_length=255)
    id_country = models.IntegerField(null=True, blank=True)
    id_regions = models.IntegerField(null=True, blank=True)
    id_city = models.IntegerField(null=True, blank=True)
    id_business_type = models.IntegerField(null=True, blank=True)
    tax_num = models.IntegerField(null=True, blank=True)
    logo_path = models.FilePathField(blank = True, null=True)
    description = models.CharField(max_length=1000)
    banned_type = models.CharField(max_length=500, blank = True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(auto_now=True)