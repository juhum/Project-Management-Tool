# Generated by Django 5.0.3 on 2024-03-11 13:28

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_projectfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectfile',
            name='file',
            field=models.FileField(upload_to=app.models.project_file_path),
        ),
    ]
