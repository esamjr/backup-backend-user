# Generated by Django 2.1.2 on 2019-04-08 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_comp', models.IntegerField()),
                ('id_hierarchy', models.IntegerField()),
                ('approval1', models.IntegerField()),
                ('approval2', models.IntegerField()),
            ],
        ),
    ]