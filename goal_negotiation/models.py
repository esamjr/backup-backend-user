from django.db import models

class goal_negotiation(models.Model):
	id_goal = models.IntegerField()
	id_goal_assignment = models.IntegerField()
	id_company = models.IntegerField()
	id_hierarchy_negotiation = models.IntegerField()
	percent = models.IntegerField()
	percent_history = models.IntegerField()
	term = models.IntegerField()
	status = models.CharField(max_length =3)
	noted = models.TextField()
	created_at = models.DateTimeField(auto_now_add= True)
	update_at = models.DateTimeField(auto_now = True)
	due_date = models.DateField()