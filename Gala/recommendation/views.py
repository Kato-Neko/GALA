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
    return render(request, 'admin_location.html', {'locations': locations})


def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            location = form.save(commit=False)

            # Fetch the address and weather data based on latitude and longitude
            if location.latitude and location.longitude:
                api_key = "ge-ea5a9c6688e4ac48"  # Replace with your actual API key
                location.address = get_address_from_coordinates(location.latitude, location.longitude, api_key)
                location.weather = get_weather_data(
                    location.latitude, location.longitude, "7334d2a0bf94493b8b894516240812"
                )

            # Save the location instance (including the weather data)
            location.save()

            # Return a JSON response with the newly added location data
            return JsonResponse({
                'status': 'success',
                'location': {
                    'id': location.id,
                    'name': location.name,
                    'description': location.description,
                    'longitude': location.longitude,
                    'latitude': location.latitude,
                    'weather': location.weather,  # Weather is now automatically populated
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

            if location.latitude and location.longitude:
                api_key = "ge-ea5a9c6688e4ac48"  # Replace with your actual API key
                location.address = get_address_from_coordinates(location.latitude, location.longitude, api_key)
                location.weather = get_weather_data(
                    location.latitude, location.longitude, "7334d2a0bf94493b8b894516240812"
                )
            location.save()
            return JsonResponse({
                'status': 'success',
                'location': {
                    'id': location.id,
                    'name': location.name,
                    'description': location.description,
                    'longitude': location.longitude,
                    'latitude': location.latitude,
                    'weather': location.weather,
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