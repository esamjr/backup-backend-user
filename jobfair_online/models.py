from django.db import models

class Jobfair(models.Model):  
  id_comp = models.IntegerField()
  id_jobs = models.IntegerField()
  date_exp = models.DateField()
  time_exp = models.TimeField()
  create_at = models.DateTimeField(auto_now_add = True)