from django.db import models

class Goal_assign(models.Model):
	id_company = models.IntegerField()	
	id_goal = models.IntegerField()
	parent = models.IntegerField()
	id_hierarchy = models.IntegerField()	
	status = models.CharField(max_length = 3)
	created_at = models.DateTimeField(auto_now_add = True)
	update_at = models.DateTimeField(auto_now = True)
	id_level = models.IntegerField()
	sisa_percent = models.IntegerField()
	sisa_allocation = models.IntegerField()
	time_allocation = models.IntegerField()