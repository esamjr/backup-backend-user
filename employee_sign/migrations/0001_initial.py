# Generated by Django 2.1.2 on 2019-01-29 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employeesign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_employee_sign', models.IntegerField(blank=True, null=True)),
                ('id_user', models.IntegerField(blank=True, null=True)),
                ('id_company', models.IntegerField(blank=True, null=True)),
                ('id_hirarchy', models.IntegerField(blank=True, null=True)),
                ('id_hirarchy_history', models.IntegerField(blank=True, null=True)),
                ('id_contract', models.IntegerField(blank=True, null=True)),
                ('id_job_contract', models.IntegerField(blank=True, null=True)),
                ('role_type', models.CharField(max_length=255)),
                ('status_type', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=3)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('delete_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
