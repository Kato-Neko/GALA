from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from django.urls import reverse_lazy

from .models import EventReminder
from .forms import EventReminderForm
from .utils import get_address_from_coordinates

from datetime import datetime, timedelta
from math import sin, cos, sqrt, atan2, radians

class ReminderCreateView(CreateView):
    model = EventReminder
    template_name = 'reminder_creater.html'
    fields = ['description', 'start_time', 'end_time', 'date', 'longitude', 'latitude', 'image']  # Include 'image'
    success_url = reverse_lazy('reminder-list')

    def form_valid(self, form):
        # Automatically fetch the address before saving
        if form.instance.latitude and form.instance.longitude:
            api_key = "ge-ea5a9c6688e4ac48"  # Replace with your actual API key
            form.instance.address = get_address_from_coordinates(form.instance.latitude, form.instance.longitude, api_key)
        return super().form_valid(form)
    
def toggle_save(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(EventReminder, pk=event_id)
        event.is_saved = not event.is_saved  # Toggle the is_saved state
        event.save()
        return JsonResponse({'success': True, 'is_saved': event.is_saved})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

class ReminderUpdateView(UpdateView):
    model = EventReminder
    template_name = 'reminder_update.php'
    fields = ['description', 'start_time', 'end_time', 'date', 'longitude', 'latitude', 'image']
    success_url = reverse_lazy('reminder-list')

    def form_valid(self, form):
        # Check if all required fields are filled out
        if not form.cleaned_data.get('description'):
            form.add_error('description', 'Description is required.')

        if not form.cleaned_data.get('start_time'):
            form.add_error('start_time', 'Start time is required.')

        if not form.cleaned_data.get('end_time'):
            form.add_error('end_time', 'End time is required.')

        if not form.cleaned_data.get('date'):
            form.add_error('date', 'Date is required.')

        if not form.cleaned_data.get('longitude') or not form.cleaned_data.get('latitude'):
            form.add_error('longitude', 'Both Longitude and Latitude are required.')

        if form.instance.latitude and form.instance.longitude:
            api_key = "ge-ea5a9c6688e4ac48"
            form.instance.address = get_address_from_coordinates(form.instance.latitude, form.instance.longitude, api_key)

        # If there are errors, return to form invalid view
        if form.errors:
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        # Log any errors for debugging purposes (optional)
        for field, error in form.errors.items():
            print(f"Error in field '{field}': {error}")

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reminder'] = self.object  # Pass the reminder instance to the template
        return context

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

            # Determine start and end datetime of the reminder
            reminder_start_datetime = datetime.combine(reminder.date, reminder.start_time)
            reminder_end_datetime = (
                datetime.combine(reminder.date, reminder.end_time) if reminder.end_time else None
            )

            # Determine reminder status
            is_happening = reminder_start_datetime <= now <= reminder_end_datetime if reminder_end_datetime else False
            is_missed = now > reminder_end_datetime if reminder_end_datetime else False

            # Calculate time remaining
            if is_happening:
                formatted_time_remaining = "Happening Now"
            elif not is_missed:
                time_remaining = reminder_start_datetime - now
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

            # Ensure no conflicting statuses
            if is_happening and is_missed:
                raise ValueError("An event cannot be both 'Happening' and 'Missed' at the same time.")

            # Store the reminder data for the list view
            reminder_data = {
                "id": reminder.event_reminder_id,
                "title": reminder.description,
                "date": reminder.date.strftime("%Y-%m-%d"),  # Format date as YYYY-MM-DD
                "start": reminder.start_time.strftime("%H:%M") if reminder.start_time else None,  # Format time as HH:MM
                "end": reminder.end_time.strftime("%H:%M") if reminder.end_time else None,
                "longitude": reminder.longitude,
                "latitude": reminder.latitude,
                "image": reminder.image.url if reminder.image else "",
                "address": reminder.address,
                "distance": f"{distance / 1000:.2f} km" if distance else "Unknown",
                "distance_value": distance if distance else float("inf"),
                "time_remaining": formatted_time_remaining,
                "time_remaining_value": (reminder_start_datetime - now).total_seconds() if not is_happening else 0,
                "is_overdue": is_missed,
                "is_happening": is_happening,
                "color": (
                    "#28a745" if is_happening else 
                    "#1b2024" if is_missed else  
                    "#00386d" 
                ),
            }

            # Append to the reminders list
            sorted_reminders.append(reminder_data)

            # Format reminder for the calendar
            calendar_events.append({
                "id": reminder.event_reminder_id,
                "title": reminder.description,
                "longitude": reminder.longitude,
                "latitude": reminder.latitude,
                "start": f"{reminder.date}T{reminder.start_time}",
                "end": f"{reminder.date}T{reminder.end_time}" if reminder.end_time else None,
                "color": (
                    "#28a745" if is_happening else  # Green for happening
                    "#1b2024" if is_missed else  # Red for missed
                    "#00386d"  # Default blue for upcoming
                ),
                "textColor": "#ffffff",
            })

        # Sort logic: prioritize happening events, then future reminders by time, and then by distance
        sorted_reminders.sort(
            key=lambda r: (
                0 if r["is_happening"] else (r["time_remaining_value"] if not r["is_overdue"] else float("inf")),
                r["distance_value"],
            )
        )

        context["reminders"] = sorted_reminders
        context["events"] = calendar_events  # Include events for the calendar
        return context
