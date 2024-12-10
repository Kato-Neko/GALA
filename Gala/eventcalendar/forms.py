from django import forms
from .models import EventReminder

class EventReminderForm(forms.ModelForm):
    class Meta:
        model = EventReminder
        fields = ['description', 'start_time', 'end_time', 'date', 'longitude', 'latitude'] 
