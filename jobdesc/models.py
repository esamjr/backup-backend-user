from django.db import models

class jobdesc(models.Model):
	id_comp = models.IntegerField(default = 0)
	id_hierarchy = models.IntegerField(unique = True)
	desc = models.CharField(max_length = 10000)

# class Logging(models.Model):
# 	activity =  models.CharField(max_length=255)
# 	executor = models.CharField(max_length=255)
# 	date_time =  models.CharField(max_length=255)
# 	vendor = models.CharField(max_length=255, blank = True, null=True)