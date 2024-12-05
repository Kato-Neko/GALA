from django.db import models

class EventReminder(models.Model):
    event_reminder_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='reminder_images/', null=True, blank=True)  # Add this field

    def __str__(self):
        return self.description
