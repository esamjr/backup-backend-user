# Generated by Django 2.1.2 on 2019-02-07 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_sign', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeesign',
            name='id_employee_sign',
        ),
    ]
