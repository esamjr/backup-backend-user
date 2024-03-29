from django.db import models
from django.utils.translation import ugettext_lazy as _


class Register(models.Model):
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255, null=True, blank=True)
    salt_password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    birth_day = models.DateField()
    primary_phone = models.CharField(max_length=255)
    primary_address = models.TextField(null=True, blank=True)
    id_country = models.IntegerField()
    id_regions = models.IntegerField()
    id_city = models.IntegerField()
    tax_num = models.CharField(max_length=20)
    ssn_num = models.BigIntegerField(default=0)
    verfied = models.IntegerField(default=0)
    url_photo = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    id_type = models.IntegerField()
    banned_type = models.CharField(max_length=255, null=True, blank=True)
    url_fb = models.CharField(max_length=255, null=True, blank=True)
    url_linkedin = models.CharField(max_length=255, null=True, blank=True)
    url_instagram = models.CharField(max_length=255, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(auto_now=True)
    attempt = models.IntegerField(default=0, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True,  blank=True)


class Domoo(models.Model):
    id_user = models.IntegerField(unique=True)
    status_domoo = models.IntegerField()


class Tokens(models.Model):
    key = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey("Register",
                                on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(_("Name"), max_length=150)
