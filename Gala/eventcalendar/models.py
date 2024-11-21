from django.db import models
import datetime

class EventReminder(models.Model):
    event_reminder_id = models.AutoField(primary_key=True)  
    description = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(null=True, blank=True)      

    def __str__(self):
        return self.description
