# Generated by Django 2.1.2 on 2019-03-19 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join_company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='joincompany',
            name='id_rec',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]