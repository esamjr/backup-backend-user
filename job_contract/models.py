from django.db import models

class Jobcontract(models.Model):

  id_company = models.IntegerField()
  id_user = models.IntegerField()
  id_contract = models.IntegerField()
  status = models.CharField(max_length = 3)
  salary = models.IntegerField()
  date_in = models.DateField()
  date_out =models.DateField()
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)