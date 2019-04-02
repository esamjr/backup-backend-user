from django.db import models


class LicenseComp (models.Model):
  Auth = (
      ('0','IsNothing'),
      ('1','IsAdmin'),
      ('2','IsUser'),
    )
  stat = (
      ('0', 'Unactive'),
      ('1', 'Active'),
      ('2', 'Deactive'),
    )
  id_hierarchy = models.IntegerField()
  attendance = models.CharField(default ='0', max_length = 10, choices = Auth)
  payroll = models.CharField(default = '0', max_length = 10, choices = Auth)
  status = models.CharField(default = '0', max_length = 10, choices = stat)
  exp_date = models.DateField(default = None)