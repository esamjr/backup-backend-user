from django.db import models
  
class Education(models.Model):  
  id_user = models.IntegerField()
  id_school = models.IntegerField(null=True,blank=True)
  name_school = models.CharField(max_length=500)
  level = models.CharField(max_length=255,null=True,blank=True)
  major = models.CharField(max_length=255,null=True,blank=True)  
  email_school = models.CharField(max_length=255)
  start_date = models.DateField()
  end_date = models.DateField()
  verified = models.CharField(max_length=3)
  url_photo = models.CharField(max_length=255,null=True,blank=True)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)