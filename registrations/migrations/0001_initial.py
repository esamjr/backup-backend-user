# Generated by Django 2.1.2 on 2019-01-30 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
                ('salt_password', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('birth_day', models.DateField()),
                ('primary_phone', models.CharField(max_length=255)),
                ('primary_address', models.TextField(blank=True, null=True)),
                ('id_country', models.IntegerField()),
                ('id_regions', models.IntegerField()),
                ('id_city', models.IntegerField()),
                ('tax_num', models.IntegerField()),
                ('url_photo', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('id_type', models.IntegerField()),
                ('banned_type', models.CharField(blank=True, max_length=255, null=True)),
                ('url_fb', models.CharField(blank=True, max_length=255, null=True)),
                ('url_linkedin', models.CharField(blank=True, max_length=255, null=True)),
                ('url_instagram', models.CharField(blank=True, max_length=255, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('delete_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
