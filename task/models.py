from django.db import models

class Task(models.Model):
	id_kpi = models.IntegerField()
	id_company = models.IntegerField()
	nama_task = models.CharField(max_length = 255)
	desc = models.TextField()
	status = models.IntegerField()
	created_hierarchy = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	# update_at = models.DateTimeField(auto_now = True)
	# id_level = models.IntegerField()
	# sisa_percent = models.IntegerField()
	# sisa_allocation = models.IntegerField()
	# time_allocation = models.IntegerField()