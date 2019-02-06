from django.db import models
from django.contrib.auth.models import User

class Vendor_api(models.Model):
	vendor_name = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	token = models.CharField(max_length = 10000, null=True, blank = True)