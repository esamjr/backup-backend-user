# Generated by Django 2.1.2 on 2020-02-13 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0002_tokens'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
            ],
        ),
    ]
