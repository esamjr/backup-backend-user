from django.db import models

class GoalPin(models.Model):
	id_company = models.IntegerField() #(int)
	id_goal = models.IntegerField() #(int)
	tipe_pinned = models.IntegerField() #(int)
	id_hierarchy = models.IntegerField() #(int)
	id_user = models.IntegerField() #(int)
	created_at = models.DateTimeField(auto_now_add = True)
