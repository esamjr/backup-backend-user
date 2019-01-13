from django.db import models

class Private(models.Model):
  id_user = models.IntegerField()
  jkk = models.CharField(max_length=255, null=True, blank=True )
  jht = models.CharField(max_length=255, null=True, blank=True)
  jp = models.CharField(max_length=255, null=True, blank=True)
  npwp = models.CharField(max_length=255, null=True, blank=True)
  nama_bank =  models.CharField(max_length=255,null=True, blank=True)
  no_rek = models.CharField(max_length=255,null=True, blank=True)
  an_rek = models.CharField(max_length=255,null=True, blank=True )
  status_parent = models.CharField(max_length=255)
  status_child = models.CharField(max_length=255)