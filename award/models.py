from django.db import models
  
class Award(models.Model):  
  id_award = models.IntegerField()
  id_user = models.IntegerField()
  id_institution = models.IntegerField()
  name_institution = models.CharField(max_length=500)
  email_institution = models.CharField(max_length=255)
  date_received = models.DateTimeField()
  verfied = models.CharField(max_length=3)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)