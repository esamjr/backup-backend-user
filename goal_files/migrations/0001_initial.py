# Generated by Django 2.1.2 on 2019-06-23 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoalFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_goal', models.IntegerField()),
                ('id_hierarchy', models.IntegerField()),
                ('id_company', models.IntegerField()),
                ('id_user', models.IntegerField()),
                ('subject', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('filetype', models.TextField()),
                ('dateadd', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(auto_now=True)),
                ('external', models.IntegerField()),
                ('external_link', models.IntegerField()),
                ('thumbnail_link', models.IntegerField()),
            ],
        ),
    ]
