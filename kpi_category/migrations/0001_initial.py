# Generated by Django 2.1.2 on 2019-06-23 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KPIcat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_company', models.IntegerField()),
                ('id_goal', models.IntegerField()),
                ('name_category', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
