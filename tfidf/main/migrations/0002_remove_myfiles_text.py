# Generated by Django 5.0.4 on 2024-04-04 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myfiles',
            name='text',
        ),
    ]