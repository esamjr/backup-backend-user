# Generated by Django 2.1.2 on 2019-03-20 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_account', '0004_auto_20190213_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='primary_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
