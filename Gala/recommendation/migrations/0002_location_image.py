# Generated by Django 5.1.4 on 2024-12-05 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='location_images/'),
        ),
    ]
