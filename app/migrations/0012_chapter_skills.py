# Generated by Django 4.2.14 on 2024-08-12 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_fib_skills_mcq_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='skills',
            field=models.TextField(blank=True),
        ),
    ]