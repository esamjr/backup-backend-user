from django.db import models

class friendlist(models.Model):
    id_user_from = models.IntegerField()
    id_user_to = models.IntegerField()
    status_type = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(auto_now=True)