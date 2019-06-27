from django.db import models

class CatGoal(models.Model):
	id_company = models.IntegerField()
	nama_categori = models.CharField(max_length = 255)
	description = models.TextField()
	status = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
