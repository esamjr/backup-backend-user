from django.db import models

class Jobs(models.Model):
  position = models.CharField(max_length = 30)
  comp_id = models.IntegerField()
  descript = models.TextField()
  sallary = models.IntegerField(blank = True, null = True)
  location = models.CharField(max_length=100)
  deadline = models.DateField()
  pref_language = models.CharField(max_length=30)
  dresscode = models.CharField(max_length=20)
  worktime = models.IntegerField()
  tunjangan = models.TextField()
  create_at = models.DateTimeField(auto_now_add = True)

class Recruitment(models.Model):
  stat = (
    (0 , 'apply'),
    (1 , 'Interviewed'),
    (2 , 'Accepted'),
    (3 , 'Decline'),
    )
  id_jobs = models.IntegerField()
  id_applicant = models.IntegerField()
  status = models.IntegerField(default = 0, choices = stat)
  descript = models.TextField()
  create_at = models.DateTimeField(auto_now = True)