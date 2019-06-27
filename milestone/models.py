from django.db import models

class Milestone(models.Model):
	id_company = models.IntegerField() #(int)
	name = models.CharField(max_length = 255) #(char)
	description = models.TextField() #(text)
	due_date = models.DateField() #(date)
	id_goal = models.IntegerField() #(int)
	color = models.CharField(max_length = 255) #(char)
	milestone_order = models.IntegerField() #(int)
	date_created = models.DateField() #(date)
	create_at = models.DateTimeField(auto_now_add = True)
