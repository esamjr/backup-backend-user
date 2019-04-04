# Generated by Django 2.1.2 on 2019-04-04 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('id_company', models.IntegerField()),
                ('id_job_contract', models.IntegerField()),
                ('name_company', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('email_company', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField()),
                ('present_date', models.IntegerField(default=0)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('verified', models.CharField(max_length=3)),
                ('recomendation', models.TextField(blank=True, null=True)),
                ('url_photo', models.CharField(blank=True, max_length=255, null=True)),
                ('satisfied', models.IntegerField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('delete_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
