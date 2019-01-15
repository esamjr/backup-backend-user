from django.db import models
  
class Award(models.Model):  
  id_user = models.IntegerField()
  id_institution = models.IntegerField(null=True,blank=True)
  name_institution = models.CharField(max_length=255,null=True,blank=True)
  award = models.CharField(max_length=255,null=True,blank=True)
  email_institution = models.CharField(max_length=255,null=True,blank=True)
  date_received = models.DateField()
  verfied = models.CharField(max_length=3)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)