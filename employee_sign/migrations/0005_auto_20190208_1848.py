# Generated by Django 2.1.2 on 2019-02-08 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_sign', '0004_auto_20190208_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesign',
            name='id_hirarchy',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='employeesign',
            name='id_job_contract',
            field=models.IntegerField(null=True),
        ),
    ]
