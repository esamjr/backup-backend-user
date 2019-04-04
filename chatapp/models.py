from django.db import models

class PersonalChat(models.Model):
	message = models.TextField()
	timestamp = models.DateTimeField(auto_now_add = True)
	sender = models.IntegerField()
	recipient = models.IntegerField(default = 0, null = True, blank = True)
	group_id = models.IntegerField(default = 0, null = True, blank = True)

class GroupChat(models.Model):
	welcome_mess = models.IntegerField(null = True ,blank = True)
	create_at = models.DateTimeField(auto_now_add = True)
	admin = models.IntegerField()

class PersonelGroupChat(models.Model):
	personel = models.IntegerField()
	join_date = models.DateTimeField(auto_now_add = True)
	group_id = models.IntegerField()
