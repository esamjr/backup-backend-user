from django.db import models

class kpi_assign(models.Model):
	id_kpi_category = models.IntegerField(default = 0)
	id_kpi_definition = models.IntegerField(default = 0)
	id_hierarchy = models.IntegerField(default = 0)
	id_company = models.IntegerField(default = 0)
	id_type = models.IntegerField(default = 0)
	bobot = models.FloatField(default = 0)
	operator = models.CharField(max_length = 255 , null = True)
	create_at = models.DateTimeField(auto_now_add = True, null = True)
