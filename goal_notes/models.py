from django.db import models

class GoalNotes(models.Model):
	id_goal = models.IntegerField() #(int)
	id_hierarchy = models.IntegerField() #(int)
	id_user = models.IntegerField() #(int)
	content = models.TextField() #(text)
	id_company = models.IntegerField() #(int)

	create_at  = models. DateTimeField(auto_now_add = True)  # (date)
	last_activity  = models. DateTimeField(auto_now = True)  # (date)
