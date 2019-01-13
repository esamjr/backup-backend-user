from django.db import models

class Region(models.Model):
   id_region = models.IntegerField()
   id_country = models.IntegerField()
   name = models.CharField(max_length=255)
   created_at = models.DateTimeField(auto_now_add=True)
   update_at = models.DateTimeField(auto_now=True)
   delete_at = models.DateTimeField(auto_now=True)