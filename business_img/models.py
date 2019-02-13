from django.db import models

class Company_img(models.Model):
   id_company = models.IntegerField()
   type_name = models.CharField(max_length=225)
   url = models.CharField(max_length = 1000)
   nomor = models.IntegerField()
   status = models.CharField(max_length=3)