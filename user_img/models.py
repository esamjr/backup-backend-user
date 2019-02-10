from django.db import models

class User_img(models.Model):
   id_user = models.IntegerField()
   type_name = models.CharField(max_length=7)
   url_ktp = models.CharField(max_length = 1000)
   url = models.CharField(max_length = 1000)
   ktp = models.IntegerField()
   nomor = models.CharField(max_length = 20)
   status = models.CharField(max_length=3)