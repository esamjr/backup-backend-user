from django.db import models

# Create your models here.
class Groups(models.Model):
    id_company = models.IntegerField()
    id_hierarchy = models.IntegerField(unique=True)
    tipe_group = models.IntegerField(default=1)
    parent_group = models.IntegerField(default=0)
    set_manage = models.IntegerField(default=0)
    set_view = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)

