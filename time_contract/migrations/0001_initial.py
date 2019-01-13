# Generated by Django 2.1.2 on 2019-01-13 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Timecontract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_time', models.IntegerField()),
                ('id_company', models.IntegerField()),
                ('name', models.CharField(max_length=500)),
                ('type_time', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('delete_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]