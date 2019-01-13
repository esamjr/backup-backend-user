from django.db import models

class Contract(models.Model):
    id_contract = models.IntegerField()
    id_company = models.IntegerField()
    id_time_contract = models.IntegerField()
    name_contract = models.CharField(max_length=255,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(auto_now=True)