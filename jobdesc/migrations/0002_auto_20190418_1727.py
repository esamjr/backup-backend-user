# Generated by Django 2.1.2 on 2019-04-18 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobdesc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobdesc',
            name='id_comp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='jobdesc',
            name='id_hierarchy',
            field=models.IntegerField(unique=True),
        ),
    ]