from django.contrib import admin
from .models import EventReminder

class EventReminderAdmin(admin.ModelAdmin):
    list_display = ('description', 'start_time', 'end_time', 'longitude', 'latitude') 

admin.site.register(EventReminder, EventReminderAdmin)