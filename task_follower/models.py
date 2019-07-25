from django.db import models

class TaskFoll(models.Model):
	id_company = models.IntegerField() # (int)
	id_task = models.IntegerField() # (int)
	id_hierarchy = models.IntegerField() # (int)
	id_user = models.IntegerField() # (int)
	create_date = models.DateTimeField(auto_now_add = True) # (date)
