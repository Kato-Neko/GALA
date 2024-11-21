from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import EventReminder

class ReminderListView(ListView):
    model = EventReminder
    template_name = 'Calendar/reminder_list.html'

class ReminderCreateView(CreateView):
    model = EventReminder
    template_name = 'Calendar/reminder_create.html'
    fields = ['description', 'start_time', 'end_time', 'date']
    success_url = reverse_lazy('reminder-list')

class ReminderUpdateView(UpdateView):
    model = EventReminder
    template_name = 'Calendar/reminder_update.html'
    fields = ['description', 'start_time', 'end_time']
    success_url = reverse_lazy('reminder-list')

class ReminderDeleteView(DeleteView):
    model = EventReminder
    template_name = 'Calendar/reminder_delete.html'
    success_url = reverse_lazy('reminder-list')
