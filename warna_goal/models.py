from django.db import models

class warna_goal(models.Model):
	id_company = models.IntegerField(default = 0)
	nama_warna= models.CharField(max_length = 255)
	kode_warna= models.CharField(max_length = 255)
	status = models.IntegerField(default = 0)
