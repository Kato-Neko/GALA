
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from user.models import Profile
from django import forms

from eventcalendar.models import EventReminder
from recommendation.models import Location
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2

import json

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'w-full bg-gray-700 text-gray-200 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50',
    }))

    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next') or '/'
            return JsonResponse({'success': True, 'redirect_url': next_url})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid username or password. Please try again.'})

    return render(request, 'authmodal.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return JsonResponse({'success': True, 'redirect_url': '/'})
        else:
            # Return the form errors as a JSON response
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = [{"message": error} for error in field_errors]
            return JsonResponse({'success': False, 'errors': errors})

    else:
        form = CustomUserCreationForm()

    return render(request, 'authmodal.html', {'form': form, 'signup_mode': True})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
def manage_account(request):
    user = request.user

    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        profile_picture = request.FILES.get('profile_picture')

        if username and username != user.username:
            user.username = username
        if email and email!= user.email:
            user.email = email
        if first_name and first_name != user.first_name:
            user.first_name = first_name
        if last_name and last_name != user.last_name:
            user.last_name = last_name
        if password:
            user.set_password(password)
            # Removed the login call here to prevent unintentional re-login
            messages.success(request, "Password updated, please log in again.")

        user.save()

        if profile_picture:
            profile.profile_picture = profile_picture
            profile.save()

        messages.success(request, "Account updated successfully!")
        return redirect('home') 

    return render(request, 'manageaccount.php', {'user': user, 'profile': profile})


@login_required
def delete_account(request):
    user = request.user
    Profile.objects.filter(user=user).delete()
    user.delete()
    messages.success(request, "Your account has been deleted successfully.")
    return redirect('home')

@csrf_exempt
def save_user_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude is not None and longitude is not None:
                # Save or use the location data (e.g., save to session or database)
                request.session['user_latitude'] = latitude
                request.session['user_longitude'] = longitude
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid location data.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000  # Convert to meters

def home(request):
    reminders = EventReminder.objects.all()
    locations = Location.objects.all()

    search_query = request.GET.get('q', '').strip()

    if search_query:
        reminders = reminders.filter(description__icontains=search_query)
        locations = locations.filter(name__icontains=search_query)

    user_latitude = request.session.get('user_latitude')
    user_longitude = request.session.get('user_longitude')

    now = datetime.now()
    combined_list = []  
    all_pins = []     

    for reminder in reminders:
        print(f"Reminder ID: {reminder.id}")  

        start_time = reminder.start_time.strftime("%I:%M %p") if reminder.start_time else ""
        end_time = reminder.end_time.strftime("%I:%M %p") if reminder.end_time else None
        distance = None

        if user_latitude and user_longitude and reminder.latitude and reminder.longitude:
            distance = calculate_distance(
                float(user_latitude), float(user_longitude),
                float(reminder.latitude), float(reminder.longitude)
            )

        reminder_start_datetime = datetime.combine(reminder.date, reminder.start_time)
        reminder_end_datetime = (
            datetime.combine(reminder.date, reminder.end_time) if reminder.end_time else None
        )
        is_happening = reminder_start_datetime <= now <= reminder_end_datetime if reminder_end_datetime else False
        is_missed = now > reminder_end_datetime if reminder_end_datetime else False

        
        all_pins.append({
            'type': 'reminder',
            'id': reminder.id,  
            'is_saved': reminder.is_saved,
            'title': reminder.description,
            'start': f"{reminder.date.strftime('%B %d, %Y')} {start_time}",
            'end': f"{reminder.date.strftime('%B %d, %Y')} {end_time}" if end_time else None,
            'latitude': reminder.latitude,
            'longitude': reminder.longitude,
            'address': reminder.address,
            'image': reminder.image.url if reminder.image else "",
            'distance': f"{int(distance)} meters" if distance and distance < 1000 else f"{distance / 1000:.2f} km" if distance else "Unknown",
            'is_happening': is_happening,
            'is_within_5km': distance and distance <= 5000  
        })


        if distance and distance <= 5000 and not is_missed:
            if is_happening:
                formatted_time_remaining = "Happening Now"
            else:
                time_remaining = reminder_start_datetime - now
                days = time_remaining.days
                hours, remainder = divmod(time_remaining.seconds, 3600)
                minutes, _ = divmod(remainder, 60)

                time_display = []
                if days > 0:
                    time_display.append(f"{days} day{'s' if days > 1 else ''}")
                if hours > 0:
                    time_display.append(f"{hours} hour{'s' if hours > 1 else ''}")
                if minutes > 0:
                    time_display.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

                formatted_time_remaining = ", ".join(time_display) + " to go"

            combined_list.append({
                'type': 'reminder',
                'id': reminder.id,  
                'is_saved': reminder.is_saved, 
                'title': reminder.description,
                'start': f"{reminder.date.strftime('%B %d, %Y')} {start_time}",
                'end': f"{reminder.date.strftime('%B %d, %Y')} {end_time}" if end_time else None,
                'latitude': reminder.latitude,
                'longitude': reminder.longitude,
                'address': reminder.address,
                'image': reminder.image.url if reminder.image else "",
                'distance': f"{int(distance)} meters" if distance and distance < 1000 else f"{distance / 1000:.2f} km" if distance else "Unknown",
                'time_remaining': formatted_time_remaining,
                'is_happening': is_happening,
            })

    combined_list.sort(key=lambda x: ('Happening Now' not in x['time_remaining'], x['time_remaining'], x['distance']))

    for location in locations:
        if location.latitude is not None and location.longitude is not None:
            distance = None
            
            if user_latitude and user_longitude:
                distance = calculate_distance(
                    float(user_latitude), float(user_longitude),
                    float(location.latitude), float(location.longitude)
                )

            all_pins.append({
                'type': 'location',
                'name': location.name,
                "is_saved": location.is_saved,
                'description': location.description,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'address': location.address,
                'image': location.image.url if location.image else "",
                'distance': f"{int(distance)} meters" if distance and distance < 1000 else f"{distance / 1000:.2f} km" if distance else "Unknown",
                'weather': location.weather,
                'is_within_5km': distance and distance <= 5000 
            })

            if distance and distance <= 5000:
                combined_list.append({
                    'type': 'location',
                    'id': location.id,
                    'name': location.name,
                    "is_saved": location.is_saved,
                    'description': location.description,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'address': location.address,
                    'image': location.image.url if location.image else "",
                    'distance': f"{int(distance)} meters" if distance and distance < 1000 else f"{distance / 1000:.2f} km" if distance else "Unknown",
                    'weather': location.weather,
                })

    combined_list_json = json.dumps(combined_list, cls=DjangoJSONEncoder)
    all_pins_json = json.dumps(all_pins, cls=DjangoJSONEncoder)

    return render(request, 'home.html', {
        'combined_list': combined_list,
        'combined_list_json': combined_list_json,
        'all_pins_json': all_pins_json,
    })

def search(request):
    query = request.GET.get('q', '').strip()
    results = []

    user_latitude = request.session.get('user_latitude')
    user_longitude = request.session.get('user_longitude')

    if query:
        now = datetime.now()

        reminders = EventReminder.objects.filter(
            description__icontains=query
        ).exclude(
            end_time__isnull=False,
            end_time__lt=now
        )

        locations = Location.objects.filter(name__icontains=query)

        for reminder in reminders:
            distance = None
            if user_latitude and user_longitude and reminder.latitude and reminder.longitude:
                distance = calculate_distance(
                    float(user_latitude), float(user_longitude),
                    float(reminder.latitude), float(reminder.longitude)
                )
            
            results.append({
                'title': reminder.description,
                'latitude': reminder.latitude,
                'longitude': reminder.longitude,
                'address': reminder.address,
                'distance': f"{int(distance)} meters" if distance and distance < 1000 else f"{distance / 1000:.2f} km" if distance else "Unknown",
                'url': f"/reminder/{reminder.id}",  
            })

        for location in locations:
            distance = None
            if user_latitude and user_longitude and location.latitude and location.longitude:
                distance = calculate_distance(
                    float(user_latitude), float(user_longitude),
                    float(location.latitude), float(location.longitude)
                )
            
            results.append({
                'title': location.name,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'address': location.address,
                'distance': f"{int(distance)} meters" if distance and distance < 1000 else f"{distance / 1000:.2f} km" if distance else "Unknown",
                'url': f"/location/{location.id}",  
            })

    return JsonResponse(results, safe=False)

@csrf_exempt
def toggle_save(request, object_id, object_type):
    if request.method == 'POST':
        if object_type == 'reminder':
            obj = get_object_or_404(EventReminder, pk=object_id)
        elif object_type == 'location':
            obj = get_object_or_404(Location, pk=object_id)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid object type'}, status=400)
        
        obj.is_saved = not obj.is_saved  
        obj.save()
        
        return JsonResponse({'success': True, 'is_saved': obj.is_saved})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def saved_posts_view(request):
    saved_reminders = EventReminder.objects.filter(is_saved=True)
    saved_locations = Location.objects.filter(is_saved=True)
    
    context = {
        'saved_reminders': saved_reminders,
        'saved_locations': saved_locations,
    }

    return render(request, 'saved.php', context)