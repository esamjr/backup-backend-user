# Generated by Django 2.1.2 on 2019-01-29 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_job_contract', models.IntegerField()),
                ('id_company', models.IntegerField()),
                ('level', models.CharField(max_length=255)),
                ('status_parent', models.CharField(max_length=255)),
                ('status_child', models.CharField(max_length=255)),
            ],
        ),
    ]
