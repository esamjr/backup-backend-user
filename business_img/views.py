from django.shortcuts import render

class Business_img(models.Model):
   id_company = models.IntegerField()
   type_name = models.CharField(max_length=225)
   url = models.CharField(max_length = 1000)