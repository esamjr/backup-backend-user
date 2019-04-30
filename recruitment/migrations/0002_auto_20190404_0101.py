# Generated by Django 2.1.2 on 2019-04-03 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitment',
            name='create_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='recruitment',
            name='status',
            field=models.IntegerField(choices=[(0, 'apply'), (1, 'Interviewed'), (2, 'Accepted'), (3, 'Decline')], default=0),
        ),
    ]