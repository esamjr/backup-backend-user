# Generated by Django 2.1.2 on 2019-01-29 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=255)),
                ('executor', models.CharField(max_length=255)),
                ('date_time', models.CharField(max_length=255)),
                ('vendor', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
