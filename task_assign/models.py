from django.db import models

class task_assign(models.Model):
	id_kpi = models.IntegerField()
	id_kpi_assign = models.IntegerField()
	id_task = models.IntegerField()
	id_hierarchy = models.IntegerField()
	id_type = models.IntegerField()
	actual_status = models.IntegerField()
	actual = models.FloatField()
	file  = models.CharField(max_length = 2000)
	created_at = models.DateTimeField(auto_now_add = True)
	update_at = models.DateTimeField(auto_now = True)
