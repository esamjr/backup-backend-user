from django.db import models
  
class Experiences(models.Model):  
  id_user = models.IntegerField()
  id_company = models.IntegerField(null=True,blank=True)
  id_job_contract = models.IntegerField(null=True,blank=True)
  name_company = models.CharField(max_length=255)
  position = models.CharField(max_length=255)
  email_company = models.CharField(max_length=255,null=True,blank=True)
  start_date = models.DateField()
  end_date = models.DateField()
  verified = models.CharField(max_length=3)
  url_photo = models.CharField(max_length=255,null=True,blank=True)
  satified = models.IntegerField(null=True,blank=True)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)