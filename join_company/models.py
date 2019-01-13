from django.db import models

class Joincompany(models.Model):
  id_user = models.IntegerField()
  id_company = models.IntegerField()
  status = models.CharField(max_length=3)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)