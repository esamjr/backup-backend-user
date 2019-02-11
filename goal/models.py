from django.db import models

class Goal(models.Model):
	id_company = models.IntegerField()
	title = models.CharField(max_length = 30)
	description = models.TextField()
	parent = models.IntegerField()
	parent_goal = models.IntegerField()
	id_hierarchy = models.IntegerField()
	id_type_goal = models.IntegerField()
	mox_jobdesk = models.IntegerField()
	max_bonus = models.IntegerField()
	status = models.CharField(max_length = 3)
	id_review_scheduler = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	update_at = models.DateTimeField(auto_now = True)
	due_date = models.DateField()
