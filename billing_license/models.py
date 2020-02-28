import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from business_account.models import Business


class BillingLicense(models.Model):
    """table for handle license from ibilling"""
    vendor_id = models.IntegerField(blank=True, null=True)
    feature_id = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=30, decimal_places=2)
    qty_license = models.IntegerField(default=0)
    term_license = models.IntegerField(default=0)
    start_date_license = models.DateField(default=datetime.date.today)
    expire_date_license = models.DateField(blank=True)
    status_license = models.BooleanField(default=False)
    id_company = models.ForeignKey(Business, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.vendor_id

    @property
    def expire_license(self):
        return self.expire_date_license

    class Meta:
        app_label = 'billing_license'
        db_table = 'billing_license'
        verbose_name = _('Billing License')
        verbose_name_plural = _('Billing License')
