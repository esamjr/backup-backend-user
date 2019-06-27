from django.db import models

class TemplateCheck(models.Model):

	id_company = models.IntegerField() #(int)
	description = models.TextField() #(text)
	create_at = models.DateTimeField(auto_now_add = True)



