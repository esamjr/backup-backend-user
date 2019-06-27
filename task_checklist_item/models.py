from django.db import models

class ItemCheck(models.Model):

	id_task = models.IntegerField() #(int)
	id_company = models.IntegerField() #(int)
	description = models.TextField() #(text)
	finished = models.IntegerField() #(int)
	dateadded = models.DateField() #(date)
	addedfrom = models.IntegerField() #(int)
	finish_from = models.IntegerField() #(int)
	listoreder = models.IntegerField() #(int)
	create_at = models.DateTimeField(auto_now_add = True)

