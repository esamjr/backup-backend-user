from django.db import models
  
class Certification(models.Model):
  id_user = models.IntegerField()
  id_institution = models.IntegerField(blank = True, null = True)
  certificate_name = models.CharField(max_length=255, blank = True, null = True)
  name_institution = models.CharField(max_length=255, blank = True, null = True)
  email_institution = models.CharField(max_length=255)
  date_received = models.DateField(blank = True, null = True)
  file_path = models.FilePathField(blank = True, null = True)
  verified = models.CharField(max_length=3)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)