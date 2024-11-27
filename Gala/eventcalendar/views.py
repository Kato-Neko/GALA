from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import EventReminder

class ReminderListView(ListView):
    model = EventReminder
    template_name = 'reminder_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add events to the context for calendar
        reminders = EventReminder.objects.all()
        events = [
            {
                "id": reminder.event_reminder_id,
                "title": reminder.description,
                "start": f"{reminder.date}T{reminder.start_time}",
                "end": f"{reminder.date}T{reminder.end_time}" if reminder.end_time else None,
            }
            for reminder in reminders
        ]
        context['events'] = events
        context['object_list'] = reminders
        return context


class ReminderCreateView(CreateView):
    model = EventReminder
    template_name = 'reminder_create.html'
    fields = ['description', 'start_time', 'end_time', 'date']
    success_url = reverse_lazy('reminder-list')

class ReminderUpdateView(UpdateView):
    model = EventReminder
    template_name = 'reminder_update.html'
    fields = ['description', 'start_time', 'end_time']
    success_url = reverse_lazy('reminder-list')

class ReminderDeleteView(DeleteView):
    model = EventReminder
    template_name = 'reminder_delete.html'
    success_url = reverse_lazy('reminder-list')

class HomeView(ListView):
    model = EventReminder
    template_name = 'home.html'  # This is the homepage template
    context_object_name = 'reminders'  # Pass this to the context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add events to the context for dynamic modal population
        reminders = EventReminder.objects.all()
        events = [
            {
                "title": reminder.description,
                "start": f"{reminder.date}T{reminder.start_time}",
                "end": f"{reminder.date}T{reminder.end_time}",
            }
            for reminder in reminders
        ]
        context['events'] = events  # Passing events for JavaScript in home.html
        return context