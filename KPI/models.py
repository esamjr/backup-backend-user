from django.db import models

class Kpi(models.Model):
	nama_kpi= models.CharField(max_length = 255)
	id_goal = models.IntegerField()
	id_company = models.IntegerField()
	standard = models.TextField()
	time_measurement = models.IntegerField()
	operator = models.CharField(max_length = 255)
	bobot = models.FloatField()
	create_hierrarchy = models.IntegerField()
	status = models.IntegerField()
	update_at = models.DateTimeField(auto_now = True)
	created_at = models.DateTimeField(auto_now_add = True)