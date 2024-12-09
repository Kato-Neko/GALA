from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Location
from .forms import LocationForm
from django.views.generic import ListView
from .utils import get_weather_data, get_address_from_coordinates

class LocationHomeView(ListView):
    model = Location
    template_name = 'home.html'
    context_object_name = 'locations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        locations = Location.objects.all()
        locations_data = [
            {
                "id": location.id,
                "name": location.name,
                "description": location.description,
                "longitude": location.longitude,
                "latitude": location.latitude,
                "weather": get_weather_data(location.latitude, location.longitude, "7334d2a0bf94493b8b894516240812"),
                "image_url": location.image.url if location.image else None,
                "address": location.address,
            }
            for location in locations
        ]
        context['locations'] = locations_data
        return context


def admin_location_view(request):
    locations = Location.objects.all()
    locations_data = [
        {
            "id": location.id,
            "name": location.name,
            "description": location.description,
            "longitude": location.longitude,
            "latitude": location.latitude,
            "image_url": location.image.url if location.image else None,
            "address": location.address,
            "weather": get_weather_data(location.latitude, location.longitude, "7334d2a0bf94493b8b894516240812"),  # Fetch real-time weather
        }
        for location in locations
    ]
    return render(request, 'admin_location.html', {'locations': locations_data})


def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            location = form.save(commit=False)

            # Fetch the address based on latitude and longitude
            if location.latitude and location.longitude:
                api_key = "ge-ea5a9c6688e4ac48"  # Replace with your actual API key
                location.address = get_address_from_coordinates(location.latitude, location.longitude, api_key)
            
            # Save the location instance
            location.save()

            # Fetch real-time weather data (dynamically returned, not saved to DB)
            weather = None
            if location.latitude and location.longitude:
                weather = get_weather_data(
                    location.latitude, location.longitude, "7334d2a0bf94493b8b894516240812"
                )

            # Return a JSON response with the newly added location data
            return JsonResponse({
                'status': 'success',
                'location': {
                    'id': location.id,
                    'name': location.name,
                    'description': location.description,
                    'longitude': location.longitude,
                    'latitude': location.latitude,
                    'weather': weather,  # Weather is dynamically fetched
                    'image_url': location.image.url if location.image else None,
                    'address': location.address,
                }
            })
    return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

def edit_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES, instance=location)
        if form.is_valid():
            location = form.save(commit=False)

            # Update address based on latitude and longitude
            if location.latitude and location.longitude:
                api_key = "ge-ea5a9c6688e4ac48"  # Replace with your actual API key
                location.address = get_address_from_coordinates(location.latitude, location.longitude, api_key)

            # Save the updated location instance
            location.save()

            # Fetch real-time weather data (dynamically returned, not saved to DB)
            weather = None
            if location.latitude and location.longitude:
                weather = get_weather_data(
                    location.latitude, location.longitude, "7334d2a0bf94493b8b894516240812"
                )

            # Return a JSON response with the updated location data
            return JsonResponse({
                'status': 'success',
                'location': {
                    'id': location.id,
                    'name': location.name,
                    'description': location.description,
                    'longitude': location.longitude,
                    'latitude': location.latitude,
                    'weather': weather,  # Weather is dynamically fetched
                    'image_url': location.image.url if location.image else None,
                    'address': location.address,
                }
            })
    return JsonResponse({'status': 'error'}, status=400)


def delete_location(request, pk):
    if request.method == 'POST':
        location = get_object_or_404(Location, pk=pk)
        location.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def recommendation_view(request):
    query = request.GET.get('search', '')
    locations = Location.objects.filter(name__icontains=query) if query else Location.objects.all()
    return render(request, 'recommendation.html', {'locations': locations, 'query': query})

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

    # Add locations to the combined list with dynamic weather
    for location in locations:
        distance = None
        weather_data = None

        if location.latitude and location.longitude:
            # Dynamically fetch weather data
            weather_data = get_weather_data(location.latitude, location.longitude, "YOUR_API_KEY")

        if user_latitude and user_longitude and location.latitude and location.longitude:
            distance = calculate_distance(
                float(user_latitude), float(user_longitude),
                float(location.latitude), float(location.longitude)
            )

        if distance is not None and distance <= 5000:  # 5 km in meters
            combined_list.append({
                'type': 'location',
                'name': location.name,
                'description': location.description,
                'longitude': location.longitude,
                'latitude': location.latitude,
                'address': location.address,
                'weather_data': weather_data,  # Add weather data
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