from django.db import models

class QuestTest(models.Model):
  id_jobs = models.IntegerField()
  serial = models.CharField(max_length = 10)
  sum_quest = models.IntegerField()
  create_at = models.DateTimeField(auto_now_add = True)

class Testform(models.Model):  
  question = models.TextField()
  answer = models.CharField(max_length = 5)
  choose_a = models.TextField()
  choose_b = models.TextField()
  choose_c = models.TextField()
  choose_d = models.TextField()
  quest_id = models.IntegerField()
  create_at = models.DateTimeField(auto_now_add = True)

class Testans(models.Model):
  id_quest = models.IntegerField()  
  id_user = models.IntegerField()
  start = models.DateTimeField(auto_now_add = True)
  score = models.IntegerField(default = 0, null= True, blank = True)
  # asnwer = models.CharField(max_length = 5)

class answ(models.Model):
  id_testans = models.IntegerField()
  id_test = models.IntegerField()
  answer = models.TextField()
  status = models.IntegerField()
