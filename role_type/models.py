from django.db import models

class Roletype(models.Model):
    id_type = models.IntegerField()
    role = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(auto_now=True)