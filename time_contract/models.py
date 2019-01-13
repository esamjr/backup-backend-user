from django.db import models

class Timecontract(models.Model):
   id_time = models.IntegerField()
   id_company = models.IntegerField()
   name = models.CharField(max_length=500)
   type_time = models.CharField(max_length=500)
   created_at = models.DateTimeField(auto_now_add=True)
   update_at = models.DateTimeField(auto_now=True)
   delete_at = models.DateTimeField(auto_now=True)