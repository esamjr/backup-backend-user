from django.db import models

class GoalSet(models.Model):
	id_goal = models.IntegerField() #(int)
	id_company = models.IntegerField() #(int)
	name = models.CharField(max_length = 255) #(char)
	value = models.TextField() #(text)

	create_at  = models. DateTimeField(auto_now_add = True)  # (date)
	last_activity  = models. DateTimeField(auto_now = True)  # (date)
