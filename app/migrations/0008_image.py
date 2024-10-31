# Generated by Django 4.2.14 on 2024-07-24 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_content_type_content_element_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='app/static/app/')),
                ('element_type', models.CharField(default='image', max_length=16)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.chapter')),
            ],
        ),
    ]