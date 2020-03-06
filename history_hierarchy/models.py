from django.db import models


class Historyhierarchy (models.Model):
  id_user = models.IntegerField()
  id_company = models.IntegerField()
  id_experience = models.IntegerField()
  id_hirarchy_history = models.IntegerField()
  name_history = models.CharField(max_length=255)  
  name_position = models.CharField(max_length=255)
  level = models.CharField(max_length=255)
  date_in = models.DateField()
  date_out = models.DateField()
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)
