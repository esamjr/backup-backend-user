from django.db import models

class KPIcat(models.Model):
	id_company = models.IntegerField() #(int)
	id_goal = models.IntegerField() #(int)
	name_category = models.CharField(max_length = 255) #(char)
	description = models.TextField() #(text)
	status = models.IntegerField() #(int)
	created_date = models.DateTimeField(auto_now_add = True)
