from django.db import models

class Email(models.Model): 
  recipient = models.CharField(max_length=500)
  sender = models.CharField(max_length=255,null=True,blank=True)
  subject = models.CharField(max_length=255,null=True,blank=True)   
  send_at = models.DateTimeField(auto_now_add=True)
  