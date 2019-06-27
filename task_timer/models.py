from django.db import models

class TaskTimer(models.Model):

	id_company = models.IntegerField() #(int)
	id_task = models.IntegerField() #(int)
	id_hierarchy = models.IntegerField() #(int)
	id_user = models.IntegerField() #(int)
	start_date = models.DateTimeField() #(datetime)
	end_date = models.DateTimeField() #(datetime)
	note = models.TextField() #(text)
	create_at = models.DateTimeField(auto_now_add = True)
