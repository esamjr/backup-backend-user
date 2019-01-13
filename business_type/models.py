from django.db import models

class Businesstype(models.Model):
    id_company = models.IntegerField()
    name_business_type = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(auto_now=True)