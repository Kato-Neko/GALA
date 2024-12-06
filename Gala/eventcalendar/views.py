from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import EventReminder
from .utils import get_address_from_coordinates
from django.views.generic import UpdateView
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
                "longitude": reminder.longitude if reminder.longitude is not None else "",
                "latitude": reminder.latitude if reminder.latitude is not None else "",
                "image": reminder.image.url if reminder.image else "",
            }
            for reminder in reminders
        ]

        context['events'] = events
        context['object_list'] = reminders
        return context

class ReminderCreateView(CreateView):
    model = EventReminder
    template_name = 'reminder_create.html'
    fields = ['description', 'start_time', 'end_time', 'date', 'longitude', 'latitude', 'image']  # Include 'image'
    success_url = reverse_lazy('reminder-list')

    def form_valid(self, form):
        # Automatically fetch the address before saving
        if form.instance.latitude and form.instance.longitude:
            api_key = "ge-ea5a9c6688e4ac48"  # Replace with your actual API key
            form.instance.address = get_address_from_coordinates(form.instance.latitude, form.instance.longitude, api_key)
        return super().form_valid(form)

class ReminderUpdateView(UpdateView):
    model = EventReminder
    fields = ['description', 'start_time', 'end_time', 'date', 'longitude', 'latitude', 'image']  # Include 'image'
    template_name = 'reminder_update.html'
    success_url = reverse_lazy('reminder-list')

    def form_valid(self, form):
        # Handle existing image if no new one is uploaded
        if 'image' not in self.request.FILES:
            form.instance.image = self.get_object().image
        
        # Fetch a new address if the coordinates are updated
        if form.instance.latitude and form.instance.longitude:
            api_key = "ge-ea5a9c6688e4ac48"  # Replace with your actual API key
            form.instance.address = get_address_from_coordinates(form.instance.latitude, form.instance.longitude, api_key)
        return super().form_valid(form)

class ReminderDeleteView(DeleteView):
    model = EventReminder
    template_name = 'reminder_delete.html'
    success_url = reverse_lazy('reminder-list')

class HomeView(ListView):
    model = EventReminder
    template_name = 'home.html' 
    context_object_name = 'reminders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add events to the context for dynamic modal population
        reminders = EventReminder.objects.all()
        events = [
            {
                "title": reminder.description,
                "start": f"{reminder.date}T{reminder.start_time}",
                "end": f"{reminder.date}T{reminder.end_time}",
                "image": reminder.image.url if reminder.image else "",
                "address": reminder.address,  # Include the address
            }
            for reminder in reminders
        ]
        context['events'] = events 
        return context
