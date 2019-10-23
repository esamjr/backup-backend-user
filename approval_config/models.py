from django.db import models


# Create your models here.
class Approval(models.Model):
	id_comp = models.IntegerField()
	id_hierarchy = models.IntegerField(unique=True)
	approval1 = models.IntegerField()
	approval2 = models.IntegerField()
	attendance1 = models.IntegerField(default=0)
	attendance2 = models.IntegerField(default=0)
	payroll1 = models.IntegerField(default=0)
	payroll2 = models.IntegerField(default=0)
