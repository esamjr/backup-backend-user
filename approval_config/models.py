from django.db import models

# Create your models here.
class Approval(models.Model):
	id_comp = models.IntegerField()
	id_hierarchy = models.IntegerField()
	approval1 = models.IntegerField()
	approval2 = models.IntegerField()