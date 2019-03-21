from django.db import models
  
class Experiences(models.Model):  
  id_user = models.IntegerField()
  id_company = models.IntegerField()
  id_job_contract = models.IntegerField()
  name_company = models.CharField(max_length=255)
  position = models.CharField(max_length=255)
  email_company = models.CharField(max_length=255,null=True,blank=True)
  start_date = models.DateField()
  present_date = models.IntegerField(default = 0)
  end_date = models.DateField(null = True, blank = True)
  verified = models.CharField(max_length=3)
  url_photo = models.CharField(max_length=255,null=True,blank=True)
  satisfied = models.IntegerField(null=True,blank=True)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)