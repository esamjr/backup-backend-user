from django.db import models

class User_img(models.Model):
   id_user = models.IntegerField()
   type_name = models.CharField(max_length=7)
   url = models.CharField(max_length = 1000)
   nomor = models.CharField(max_length = 20)
   status = models.CharField(max_length=3)