from django.db import models

class type_goal(models.Model):
	id_company = models.IntegerField()
	types = models.CharField(max_length = 30)
	job_desk = models.IntegerField()
	bonus = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	update_at = models.DateTimeField(auto_now = True)