# Generated by Django 2.1.2 on 2019-02-05 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='parent_company',
        ),
    ]