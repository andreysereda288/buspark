# Generated by Django 3.1.5 on 2021-01-13 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buspark', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='driver',
            field=models.ManyToManyField(to='buspark.Driver'),
        ),
    ]
