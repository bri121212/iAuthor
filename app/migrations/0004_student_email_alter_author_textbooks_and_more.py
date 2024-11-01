# Generated by Django 5.0.6 on 2024-07-23 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_author_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='author',
            name='textbooks',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='elements',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='fib',
            name='hint',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mcq',
            name='hint',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='textbooks',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='textbook',
            name='published_chapters',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='textbook',
            name='unpublished_chapters',
            field=models.TextField(blank=True),
        ),
    ]
