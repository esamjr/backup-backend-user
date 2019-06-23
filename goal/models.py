from django.db import models

class Goal(models.Model):
	id_company = models.IntegerField()
	name = models.CharField(max_length = 255)
	description = models.TextField()
	status = models.IntegerField()
	start_date = models.DateField()
	end_date = models.DateField()
	progress = models.IntegerField()
	progress_from_task = models.IntegerField()
	id_category_goal = models.IntegerField()
	id_warna_goal = models.IntegerField()
	create_hierarchy = models.IntegerField()
	create_user = models.IntegerField()
	create_date = models.DateTimeField(auto_now_add = True)

# id_company (int)
# name (char)
# description (text)
# status (int)
# start_date(date)
# end_date(date)
# progress (int)
# progress_from_task (int)
# id_category_goal (int)
# id_warna_goal (int)
# create_hierarchy (int)
# create_user(int)
# create_date (date)

# 	id_company = models.IntegerField()
# 	title = models.CharField(max_length = 30)
# 	description = models.TextField()
# 	percent = models.IntegerField()
# 	parent_goal = models.IntegerField()
# 	id_hierarchy = models.IntegerField()
# 	id_type_goal = models.IntegerField()
# 	max_jobdesk = models.IntegerField()
# 	max_bonus = models.IntegerField()
# 	status = models.CharField(max_length = 3)
# 	id_review_scheduler = models.IntegerField()
# 	created_at = models.DateTimeField(auto_now_add = True)
# 	update_at = models.DateTimeField(auto_now = True)
# 	due_date = models.DateField()
# 	id_level = models.IntegerField()
# 	time_allocation = models.IntegerField()
# 	sisa_allocation = models.IntegerField()

class Goal2(models.Model):
	id_company = models.IntegerField()
	id_time_period = models.IntegerField()
	id_category_goal = models.IntegerField()
	spt_priority = models.IntegerField()
	start = models.DateField()
	end = models.DateField()
	create_hierarchy = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	update_at = models.DateTimeField(auto_now = True)















