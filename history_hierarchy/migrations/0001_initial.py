# Generated by Django 2.1.2 on 2019-01-30 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Historyhierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_company', models.IntegerField()),
                ('id_hirarchy_history', models.IntegerField()),
                ('name_history', models.CharField(max_length=255)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('delete_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
