from django.db import models

class Interview(models.Model):	
	id_rec = models.IntegerField()
	date = models.DateField()
	time = models.CharField(max_length = 10)
	place = models.CharField(max_length = 100)
	email_user = models.CharField(max_length = 50)
	email_comp = models.CharField(max_length = 100)
	create_at = models.DateTimeField(auto_now_add=True)