from django.contrib import admin
from .models import EventReminder

class EventReminderAdmin(admin.ModelAdmin):
    list_display = ('event_reminder_id', 'description', 'start_time', 'end_time', 'longitude', 'latitude')  # Include event_reminder_id

admin.site.register(EventReminder, EventReminderAdmin)