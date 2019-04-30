from django.db import models

class Hierarchy(models.Model):
    id_level = models.IntegerField()
    id_company = models.IntegerField()
    id_user = models.IntegerField(default = 0)
    assistant = models.IntegerField(default = 0)
    id_hirarchy = models.IntegerField()
    id_hirarchy_history = models.IntegerField()
    level = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    parent = models.CharField(max_length=100)
    id_po_sku_active = models.IntegerField()
    status = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(auto_now=True)