from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import EventReminder

def get_place_name(latitude, longitude):
        return "Sample Location"


class ReminderListView(ListView):
    model = EventReminder
    template_name = 'reminder_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reminders = EventReminder.objects.all()
        events = []
        for reminder in reminders:
            latitude = reminder.latitude
            longitude = reminder.longitude
            location = get_place_name(latitude, longitude) 
            print(f"DEBUG: Adding event with location '{location}'") 
            events.append({
                "id": reminder.event_reminder_id,
                "title": reminder.description,
                "start": f"{reminder.date}T{reminder.start_time}",
                "end": f"{reminder.date}T{reminder.end_time}" if reminder.end_time else None,
                "longitude": longitude,
                "latitude": latitude,
                "location": location,
            })
        context['reminders'] = events
        return context

    
class ReminderCreateView(CreateView):
    model = EventReminder
    template_name = 'reminder_create.html'
    fields = ['description', 'start_time', 'end_time', 'date', 'longitude', 'latitude']
    success_url = reverse_lazy('reminder-list')

class ReminderUpdateView(UpdateView):
    model = EventReminder
    template_name = 'reminder_update.html'
    fields = ['description', 'start_time', 'end_time', 'longitude', 'latitude']
    success_url = reverse_lazy('reminder-list')

class ReminderDeleteView(DeleteView):
    model = EventReminder
    template_name = 'reminder_delete.html'
    success_url = reverse_lazy('reminder-list')

