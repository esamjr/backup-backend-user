# Generated by Django 2.1.2 on 2019-02-11 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='goal_negotiation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_goal', models.IntegerField()),
                ('id_parent_goal_negotiation', models.IntegerField()),
                ('id_company', models.IntegerField()),
                ('id_hierarchy_negotiation', models.IntegerField()),
                ('percent', models.IntegerField()),
                ('percent_history', models.IntegerField()),
                ('term', models.IntegerField()),
                ('status', models.CharField(max_length=3)),
                ('noted', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateField()),
                ('id_level', models.IntegerField()),
                ('sisa_percent', models.IntegerField()),
                ('time_allocation', models.IntegerField()),
                ('sisa_allocation', models.IntegerField()),
                ('sum_percent', models.IntegerField()),
                ('history_allocation', models.IntegerField()),
                ('sum_allocation', models.IntegerField()),
            ],
        ),
    ]
