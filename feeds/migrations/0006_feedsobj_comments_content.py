# Generated by Django 2.1.2 on 2019-08-09 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0005_auto_20190809_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedsobj',
            name='comments_content',
            field=models.TextField(default=''),
        ),
    ]