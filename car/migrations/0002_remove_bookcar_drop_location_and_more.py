# Generated by Django 5.0.2 on 2024-03-15 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookcar',
            name='drop_location',
        ),
        migrations.RemoveField(
            model_name='bookcar',
            name='pickup_location',
        ),
    ]
