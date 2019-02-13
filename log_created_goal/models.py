from django.db import models

class log_goal(models.Model):
	id_company = models.IntegerField()	
	id_goal = models.IntegerField()
	id_hierarchy = models.IntegerField()
	id_user = models.IntegerField()
	created_at = models.CharField(max_length = 255)
	update_at = models.CharField(max_length = 255, default = '**')