# Generated by Django 3.1.5 on 2021-01-17 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buspark', '0003_auto_20210114_0041'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bus',
            unique_together={('name', 'bus_model')},
        ),
    ]
