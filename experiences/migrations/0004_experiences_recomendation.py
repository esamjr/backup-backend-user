# Generated by Django 2.1.2 on 2019-03-28 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0003_auto_20190322_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiences',
            name='recomendation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
