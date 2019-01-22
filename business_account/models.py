from django.db import models

class Business(models.Model):
    id_user = models.IntegerField()
    
    company_name = models.CharField(max_length=255)
    email = models.CharField (max_length=255, unique=True, null = True)
    primary_phone = models.IntegerField(null = True)
    primary_address = models.CharField(max_length=255, null = True)
    id_country = models.IntegerField(null=True, blank=True)
    id_regions = models.IntegerField(null=True, blank=True)
    id_city = models.IntegerField(null=True, blank=True)
    id_business_type = models.IntegerField(null=True, blank=True)
    tax_num = models.IntegerField(null=True, blank=True)
    logo_path = models.FilePathField(blank = True, null=True)
    description = models.CharField(max_length=1000, null = True)
    banned_type = models.CharField(max_length=500, blank = True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(auto_now=True)