# Generated by Django 5.1.1 on 2024-12-09 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0004_alter_location_options_remove_location_weather_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='weather',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
