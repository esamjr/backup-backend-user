# Generated by Django 2.1.2 on 2019-05-27 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='kpi_assign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_kpi', models.IntegerField()),
                ('id_hierarchy', models.IntegerField()),
                ('id_company', models.IntegerField()),
                ('id_type', models.IntegerField()),
                ('bobot', models.FloatField()),
                ('operator', models.CharField(max_length=255)),
            ],
        ),
    ]
