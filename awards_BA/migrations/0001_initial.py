# Generated by Django 2.1.2 on 2019-03-05 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AwardBA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('id_institution', models.IntegerField(blank=True, null=True)),
                ('award', models.CharField(blank=True, max_length=255, null=True)),
                ('name_institution', models.CharField(blank=True, max_length=255, null=True)),
                ('email_institution', models.CharField(blank=True, max_length=255, null=True)),
                ('date_received', models.DateField()),
                ('verified', models.CharField(default='null', max_length=3)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('delete_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]