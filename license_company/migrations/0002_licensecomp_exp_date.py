# Generated by Django 2.1.2 on 2019-04-02 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license_company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='licensecomp',
            name='exp_date',
            field=models.DateField(default=None),
        ),
    ]
