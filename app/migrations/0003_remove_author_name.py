# Generated by Django 5.0.6 on 2024-07-23 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='name',
        ),
    ]
