# Generated by Django 2.1.2 on 2020-02-11 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedsobj',
            name='content',
            field=models.TextField(),
        ),
    ]
