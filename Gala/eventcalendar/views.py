from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .utils import get_address_from_coordinates
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import EventReminder

from datetime import datetime, timedelta
from math import sin, cos, sqrt, atan2, radians

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

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371 
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000 

class ReminderListView(ListView):
    model = EventReminder
    template_name = 'reminder_list.php'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reminders = EventReminder.objects.all()
        user_latitude = self.request.session.get('user_latitude')
        user_longitude = self.request.session.get('user_longitude')
        now = datetime.now()

        sorted_reminders = []
        calendar_events = []

        for reminder in reminders:
            # Calculate distance if user location is available
            distance = None
            if user_latitude and user_longitude and reminder.latitude and reminder.longitude:
                distance = calculate_distance(
                    float(user_latitude), float(user_longitude),
                    float(reminder.latitude), float(reminder.longitude)
                )

            # Calculate time remaining
            reminder_datetime = datetime.combine(reminder.date, reminder.start_time)
            time_remaining = reminder_datetime - now

            # Format time dynamically, skipping 0 days or hours
            if time_remaining.total_seconds() > 0:
                days = time_remaining.days
                hours, remainder = divmod(time_remaining.seconds, 3600)
                minutes, _ = divmod(remainder, 60)

                time_parts = []
                if days > 0:
                    time_parts.append(f"{days} days")
                if hours > 0:
                    time_parts.append(f"{hours} hours")
                if minutes > 0:
                    time_parts.append(f"{minutes} minutes")

                formatted_time_remaining = " ".join(time_parts)
            else:
                formatted_time_remaining = "Missed"

            # Store the reminder data for the list view
            reminder_data = {
                "id": reminder.event_reminder_id,
                "title": reminder.description,
                "start": f"{reminder.date}T{reminder.start_time}",
                "end": f"{reminder.date}T{reminder.end_time}" if reminder.end_time else None,
                "longitude": reminder.longitude,
                "latitude": reminder.latitude,
                "image": reminder.image.url if reminder.image else "",
                "address": reminder.address,
                "distance": f"{distance / 1000:.2f} km" if distance else "Unknown",
                "distance_value": distance if distance else float("inf"),  # Use infinity for unknown distances
                "time_remaining": formatted_time_remaining,
                "time_remaining_value": time_remaining.total_seconds(),  # For sorting purposes
                "is_overdue": time_remaining.total_seconds() < 0,
            }

            # Append to the reminders list
            sorted_reminders.append(reminder_data)

            # Format reminder for the calendar
            calendar_events.append({
                "id": reminder.event_reminder_id,
                "title": reminder.description,
                "start": f"{reminder.date}T{reminder.start_time}",
                "end": f"{reminder.date}T{reminder.end_time}" if reminder.end_time else None,
                "color": "#b70000" if reminder_data["is_overdue"] else "#00386d",  # Highlight missed events in red
                "textColor": "#ffffff", 
            })

        # Sort logic: prioritize future reminders by time first, then by distance
        sorted_reminders.sort(
            key=lambda r: (
                r["time_remaining_value"] if not r["is_overdue"] else float("inf"),  # Time for non-overdue events
                r["distance_value"],  # Then by distance
            )
        )

        context["reminders"] = sorted_reminders
        context["events"] = calendar_events  # Include events for the calendar
        return context
