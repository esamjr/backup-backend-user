from django.db import models

class Typetime(models.Model):
   id_type_time = models.IntegerField()
   id_company = models.IntegerField()
   name = models.CharField(max_length=500)
   created_at = models.DateTimeField(auto_now_add=True)
   update_at = models.DateTimeField(auto_now=True)
   delete_at = models.DateTimeField(auto_now=True)