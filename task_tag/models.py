from django.db import models

class TaskTag(models.Model):
	id_company = models.IntegerField() #(int)
	id_task = models.IntegerField()
	id_tag = models.IntegerField()
	create_at = models.DateTimeField(auto_now_add = True)



