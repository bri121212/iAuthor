# Generated by Django 4.2.14 on 2024-08-11 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_response_chapter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('textbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.textbook')),
            ],
        ),
    ]
