from django.db import models

class log_goal(models.Model):
	id_company = models.IntegerField()	
	id_goal = models.IntegerField()
	id_hierarchy = models.IntegerField()
	id_user = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	update_at = models.DateTimeField(auto_now = True)