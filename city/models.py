from django.db import models

class City(models.Model):
   id_region = models.IntegerField()
   id_city = models.IntegerField()
   name = models.CharField(max_length=255)
   created_at = models.DateTimeField(auto_now_add=True)
   update_at = models.DateTimeField(auto_now=True)
   delete_at = models.DateTimeField(auto_now=True)