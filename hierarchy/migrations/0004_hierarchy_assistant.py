# Generated by Django 2.1.2 on 2019-04-22 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hierarchy', '0003_auto_20190208_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='hierarchy',
            name='assistant',
            field=models.IntegerField(default=0),
        ),
    ]
