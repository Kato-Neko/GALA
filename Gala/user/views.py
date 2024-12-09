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
from django.db.models import Q
from user.models import Profile
from django import forms

from eventcalendar.models import EventReminder
from recommendation.models import Location
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from recommendation.utils import get_weather_data

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
    a = sin(dlat / 2) * 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000  # Convert to meters

def home(request):
    reminders = EventReminder.objects.all()
    locations = Location.objects.all()

    # Retrieve user's current location from the session
    user_latitude = request.session.get('user_latitude')
    user_longitude = request.session.get('user_longitude')

    combined_list = []

    # Add reminders to the combined list
    for reminder in reminders:
        start_time = reminder.start_time.strftime("%I:%M %p") if reminder.start_time else ""
        end_time = reminder.end_time.strftime("%I:%M %p") if reminder.end_time else None
        distance = None

        if user_latitude and user_longitude and reminder.latitude and reminder.longitude:
            distance = calculate_distance(
                float(user_latitude), float(user_longitude),
                float(reminder.latitude), float(reminder.longitude)
            )

        if distance is not None and distance <= 5000:  # 5 km in meters
            combined_list.append({
                'type': 'reminder',
                'title': reminder.description,
                'start': f"{reminder.date.strftime('%B %d, %Y')} {start_time}",
                'end': f"{reminder.date.strftime('%B %d, %Y')} {end_time}" if end_time else None,
                'longitude': reminder.longitude if reminder.longitude is not None else "",
                'latitude': reminder.latitude if reminder.latitude is not None else "",
                'address': reminder.address,
                'image': reminder.image.url if reminder.image else "",  # Include image URL
                'distance_value': distance,  # Add raw distance for sorting
                'distance': f"{distance / 1000:.2f} km",  # Convert to km for display
            })

    # Add locations to the combined list
    for location in locations:
        distance = None
        weather = None  # Initialize weather variable
        if user_latitude and user_longitude and location.latitude and location.longitude:
            distance = calculate_distance(
                float(user_latitude), float(user_longitude),
                float(location.latitude), float(location.longitude)
            )
            # Fetch dynamic weather data
            weather = get_weather_data(
                location.latitude, location.longitude, "7334d2a0bf94493b8b894516240812"
            )

        if distance is not None and distance <= 5000:  # 5 km in meters
            combined_list.append({
                'type': 'location',
                'name': location.name,
                'description': location.description,
                'longitude': location.longitude,
                'latitude': location.latitude,
                'address': location.address,
                'weather': weather,  # Add dynamically fetched weather data
                'distance_value': distance,  # Add raw distance for sorting
                'distance': f"{distance / 1000:.2f} km",  # Convert to km for display
            })

    # Sort the combined list by distance
    combined_list.sort(key=lambda x: x['distance_value'])

    combined_list_json = json.dumps(combined_list, cls=DjangoJSONEncoder)

    return render(request, 'home.html', {
        'combined_list': combined_list,
        'combined_list_json': combined_list_json,
    })

def search(request):
    query = request.GET.get('q', '').strip()
    results = []

    # Get user's current location from the session
    user_latitude = request.session.get('user_latitude')
    user_longitude = request.session.get('user_longitude')

    if query:
        now = datetime.now()

        # Search in EventReminder and exclude missed reminders
        reminders = EventReminder.objects.filter(
            description__icontains=query
        ).exclude(
            end_time__isnull=False,
            end_time__lt=now
        )

        # Search in Location models
        locations = Location.objects.filter(name__icontains=query)

        # Add reminders to results
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
                'url': f"/reminder/{reminder.event_reminder_id}",  # Adjust the URL as needed
            })

        # Add locations to results
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
                'url': f"/location/{location.id}",  # Adjust the URL as needed
            })

    return JsonResponse(results, safe=False)