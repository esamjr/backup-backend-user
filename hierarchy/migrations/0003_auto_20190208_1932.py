# Generated by Django 2.1.2 on 2019-02-08 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hierarchy', '0002_auto_20190208_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hierarchy',
            name='id_user',
            field=models.IntegerField(default=0),
        ),
    ]
