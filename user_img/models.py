from django.db import models

class User_img(models.Model):
   id_user = models.IntegerField()
   type_name = models.CharField(max_length=7)
   url_ktp = models.CharField(max_length = 1000)
   url_npwp = models.CharField(max_length = 1000, default = '***')
   no_ktp = models.BigIntegerField()
   no_npwp = models.CharField(max_length = 20,default = '**')
   status = models.CharField(max_length=3, default = '*')