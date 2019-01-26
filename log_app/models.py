from django.db import models

class Logging(models.Model):
	activity =  models.CharField(max_length=255)
	executor = models.CharField(max_length=255)
	date_time =  models.CharField(max_length=255)
	vendor = models.CharField(max_length=255, blank = True, null=True)