# Generated by Django 5.0.4 on 2024-07-12 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='about',
            field=models.TextField(default='None'),
        ),
    ]
