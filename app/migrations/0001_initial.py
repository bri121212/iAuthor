# Generated by Django 5.0.6 on 2024-07-23 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('isPublished', models.BooleanField(default=False)),
                ('elements', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('textbooks', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Textbook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('published_chapters', models.TextField()),
                ('unpublished_chapters', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('content_type', models.CharField(choices=[('paragraph', 'Paragraph'), ('note', 'Note'), ('example', 'Example'), ('subsection', 'Subsection'), ('image', 'Image'), ('video', 'Video')], max_length=16)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='FIB',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('hint', models.TextField()),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Likert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('positive', models.TextField()),
                ('negative', models.TextField()),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='MCQ',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('options', models.TextField()),
                ('answer', models.TextField()),
                ('hint', models.TextField()),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question_type', models.CharField(choices=[('mcq', 'MCQ'), ('fib', 'FIB'), ('likert', 'Likert')], max_length=16)),
                ('question', models.IntegerField()),
                ('answer', models.TextField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='textbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.textbook'),
        ),
    ]
