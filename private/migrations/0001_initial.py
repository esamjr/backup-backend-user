# Generated by Django 2.1.2 on 2019-01-29 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Private',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('jkk', models.CharField(blank=True, max_length=255, null=True)),
                ('jht', models.CharField(blank=True, max_length=255, null=True)),
                ('jp', models.CharField(blank=True, max_length=255, null=True)),
                ('npwp', models.CharField(blank=True, max_length=255, null=True)),
                ('nama_bank', models.CharField(blank=True, max_length=255, null=True)),
                ('no_rek', models.CharField(blank=True, max_length=255, null=True)),
                ('an_rek', models.CharField(blank=True, max_length=255, null=True)),
                ('status_parent', models.CharField(max_length=255)),
                ('status_child', models.CharField(max_length=255)),
            ],
        ),
    ]
