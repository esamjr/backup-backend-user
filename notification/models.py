from django.db import models

class Notification(models.Model):    
    id_user = models.IntegerField()
    messages = models.CharField(max_length=100)
    status = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)