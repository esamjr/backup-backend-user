# Generated by Django 2.1.2 on 2019-02-06 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company_img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_company', models.IntegerField()),
                ('type_name', models.CharField(max_length=225)),
                ('url', models.CharField(max_length=1000)),
                ('nomor', models.IntegerField()),
                ('status', models.CharField(max_length=3)),
            ],
        ),
    ]