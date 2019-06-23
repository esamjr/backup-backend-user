from django.db import models

class Tag(models.Model):
	id_company = models.IntegerField() #(int)
	name_tag = models.CharField(max_length = 255)
	create_at = models.DateTimeField(auto_now_add = True)
