from django.db import models

class review_scheduler(models.Model):
	id_company = models.IntegerField()
	yearly = models.CharField(max_length = 5)
	type_scheduller = models.CharField(max_length=10)
	deadline = models.DateField()
	created_at = models.DateTimeField(auto_now_add = True)
	update_at = models.DateTimeField(auto_now = True)