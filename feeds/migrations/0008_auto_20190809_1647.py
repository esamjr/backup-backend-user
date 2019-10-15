# Generated by Django 2.1.2 on 2019-08-09 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0007_userlike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlike',
            name='FeedsObjs',
        ),
        migrations.AddField(
            model_name='userlike',
            name='feedsobjs',
            field=models.ManyToManyField(blank=True, related_name='user_like', to='feeds.FeedsObj'),
        ),
    ]