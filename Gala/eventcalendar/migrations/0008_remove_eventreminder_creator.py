# Generated by Django 5.1.1 on 2024-12-07 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventcalendar', '0007_alter_eventreminder_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventreminder',
            name='creator',
        ),
    ]
