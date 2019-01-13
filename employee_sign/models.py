from django.db import models

class Employeesign(models.Model):
  id_employee_sign = models.IntegerField(blank=True,null=True)
  id_user = models.IntegerField(blank=True,null=True)
  id_company = models.IntegerField(blank=True,null=True)
  id_hirarchy = models.IntegerField(blank=True,null=True)
  id_hirarchy_history = models.IntegerField(blank=True,null=True)
  id_contract = models.IntegerField(blank=True,null=True)
  id_job_contract = models.IntegerField(blank=True,null=True)
  role_type = models.CharField(max_length=255)
  status_type = models.CharField(max_length=255)
  status = models.CharField(max_length=3)
  create_at = models.DateTimeField(auto_now_add=True)
  update_at = models.DateTimeField(auto_now=True)
  delete_at = models.DateTimeField(auto_now=True)