# Generated by Django 2.1.2 on 2019-02-08 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_sign', '0005_auto_20190208_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesign',
            name='id_hirarchy_history',
            field=models.IntegerField(null=True),
        ),
    ]