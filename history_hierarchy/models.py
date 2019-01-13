from django.db import models

class Historyhierarchy (models.Model):
  id_company = models.IntegerField()
  id_hirarchy_history = models.IntegerField()
  name_history = models.CharField(max_length=255)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)