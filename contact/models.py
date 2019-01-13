from django.db import models

class Contact(models.Model):
    id_user = models.IntegerField()
    name = models.CharField(max_length=255)
    type_phone = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address_type = models.CharField(max_length=255)
    address = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)