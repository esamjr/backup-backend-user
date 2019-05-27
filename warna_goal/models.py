from django.db import models

class warna_goal(models.Model):
	nama_warna= models.CharField(max_length = 255)
	kode_warna= models.CharField(max_length = 255)
	# id_goal = models.IntegerField()
	# parent = models.IntegerField()
	# id_hierarchy = models.IntegerField()	
	# status = models.CharField(max_length = 3)
	# created_at = models.DateTimeField(auto_now_add = True)
	# update_at = models.DateTimeField(auto_now = True)
	# id_level = models.IntegerField()
	# sisa_percent = models.IntegerField()
	# sisa_allocation = models.IntegerField()
	# time_allocation = models.IntegerField()