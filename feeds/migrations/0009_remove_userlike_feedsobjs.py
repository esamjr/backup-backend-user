# Generated by Django 2.1.2 on 2019-08-09 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0008_auto_20190809_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlike',
            name='feedsobjs',
        ),
    ]