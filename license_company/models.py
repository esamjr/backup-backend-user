from django.db import models


class LicenseComp (models.Model):
  Auth = (
      ('0','IsNothing'),
      ('1','IsUser'),
      ('2','IsAdmin'),
    )
  stat = (
      ('0', 'Unactive'),
      ('1', 'Active'),
      ('2', 'Deactive'),
    )
  id_hierarchy = models.IntegerField(unique = True)
  attendance = models.CharField(default ='0', max_length = 10, choices = Auth)
  payroll = models.CharField(default = '0', max_length = 10, choices = Auth)
  erp = models.CharField(default = '0', max_length = 10, choices = Auth)
  status = models.CharField(default = '0', max_length = 10, choices = stat)
  expr_date = models.DateField(null = True, blank = True)
  id_comp = models.IntegerField()