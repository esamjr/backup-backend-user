from django.db import models

class Level(models.Model):
  id_job_contract = models.IntegerField()
  id_company = models.IntegerField()
  level = models.CharField(max_length=255)
  status_parent = models.CharField(max_length=255)
  status_child = models.CharField(max_length=255)