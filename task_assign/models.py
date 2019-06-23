from django.db import models

class task_assign(models.Model):
	id_kpi_definition = models.IntegerField(default = 0)
	id_kpi_assign = models.IntegerField(default = 0)
	id_task = models.IntegerField(default = 0)
	id_hierarchy = models.IntegerField(default = 0)
	id_type = models.IntegerField(default = 0)
	actual_status = models.IntegerField(default = 0)
	actual = models.FloatField(default = 0)
	id_company = models.IntegerField(default = 0)
	id_user  = models.IntegerField(default = 0)
	id_kpi_category = models.IntegerField() 
	created_at = models.DateTimeField(auto_now_add = True)
	update_at = models.DateTimeField(auto_now = True)
