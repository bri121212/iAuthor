# Generated by Django 5.0.6 on 2024-07-24 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_content_chapter_content_content_type_fib_chapter_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='content_type',
            new_name='element_type',
        ),
    ]