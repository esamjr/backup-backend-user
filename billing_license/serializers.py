from rest_framework import serializers

from .models import BillingLicense


class BillingLicenseAllDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingLicense
        fields = '__all__'


class BillingLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingLicense
        fields = ['vendor_id', 'feature_id', 'price', 'qty_license', 'term_license', 'start_date_license',
                  'expire_date_license', 'status_license', 'id_company']

