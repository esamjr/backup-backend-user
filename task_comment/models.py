from django.db import models

class TaskComm(models.Model):
	# # id_company (int)
	# id_hierarchy (int)
	# id_user (int)
	# id_task (int)
	# # content (text)
	# # id_file (int)
	# # datedadd (date)
	id_company = models.IntegerField() #(int)
	id_hierarchy = models.IntegerField() #(text)
	id_user = models.IntegerField() #(date)
	id_task = models.IntegerField() #(int)
	content = models.TextField()
	id_file = models.IntegerField() #(int)
	datedadd = models.DateField() #(date)
	create_at = models.DateTimeField(auto_now_add = True)
