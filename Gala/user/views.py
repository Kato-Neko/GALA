from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from user.models import Profile
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from eventcalendar.models import EventReminder
from recommendation.models import Location
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

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000  # Convert to meters

def home(request):
    from math import radians, sin, cos, sqrt, atan2

    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the Earth in km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c * 1000  # Convert to meters

    user_lat = float(request.GET.get('latitude', 0))  # Replace 0 with a default latitude
    user_lon = float(request.GET.get('longitude', 0))  # Replace 0 with a default longitude

    reminders = EventReminder.objects.all()
    locations = Location.objects.all()

    combined_list = []

    for reminder in reminders:
        if reminder.latitude is not None and reminder.longitude is not None:
            distance = calculate_distance(user_lat, user_lon, reminder.latitude, reminder.longitude)
            distance_str = f"{int(distance)} meters" if distance < 1000 else f"{distance / 1000:.2f} kilometers"
            combined_list.append({
                'type': 'reminder',
                'description': reminder.description,
                'latitude': reminder.latitude,
                'longitude': reminder.longitude,
                'date': reminder.date,
                'start_time': reminder.start_time,
                'distance': distance_str,
            })

    for location in locations:
        if location.latitude is not None and location.longitude is not None:
            distance = calculate_distance(user_lat, user_lon, location.latitude, location.longitude)
            distance_str = f"{int(distance)} meters" if distance < 1000 else f"{distance / 1000:.2f} kilometers"
            combined_list.append({
                'type': 'location',
                'name': location.name,
                'description': location.description,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'weather': location.weather,
                'distance': distance_str,
            })

    combined_list.sort(key=lambda x: float(x['distance'].split()[0]))

    return render(request, 'home.html', {'combined_list': combined_list})
