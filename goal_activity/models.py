from django.db import models

class ActGoal(models.Model):
	id_goal = models.IntegerField() #(int)
	id_company = models.IntegerField() #(int)
	id_hierarchy = models.IntegerField() #(int)
	id_user = models.IntegerField() #(int)
	division = models.CharField(max_length = 255) #(char)
	full_name = models.CharField(max_length  = 255) #(char)
	description_key = models.CharField(max_length =255) #(char)
	addtional_data = models.TextField() #(text)
	created_date = models.DateTimeField(auto_now_add = True) #(date)
