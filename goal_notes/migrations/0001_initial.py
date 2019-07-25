# Generated by Django 2.1.2 on 2019-06-23 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoalNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_goal', models.IntegerField()),
                ('id_hierarchy', models.IntegerField()),
                ('id_user', models.IntegerField()),
                ('content', models.TextField()),
                ('id_company', models.IntegerField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
