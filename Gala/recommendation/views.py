from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Location
from .forms import LocationForm
from django.views.generic import ListView
from .utils import get_weather_data, get_address_from_coordinates
from django.views.decorators.csrf import csrf_exempt


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
            "weather": get_weather_data(location.latitude, location.longitude, "7334d2a0bf94493b8b894516240812"), 
        }
        for location in locations
    ]
    return render(request, 'admin_location.html', {'locations': locations_data})

def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            location = form.save(commit=False)

            if location.latitude and location.longitude:
                api_key = "ge-ea5a9c6688e4ac48"  
                location.address = get_address_from_coordinates(location.latitude, location.longitude, api_key)
            
            if location.latitude and location.longitude:
                weather = get_weather_data(location.latitude, location.longitude, "7334d2a0bf94493b8b894516240812")
                location.weather = weather  
            
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
    return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)


def edit_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES, instance=location)
        if form.is_valid():
            location = form.save(commit=False)

            if location.latitude and location.longitude:
                api_key = "ge-ea5a9c6688e4ac48" 
                location.address = get_address_from_coordinates(location.latitude, location.longitude, api_key)

            if location.latitude and location.longitude:
                weather = get_weather_data(location.latitude, location.longitude, "7334d2a0bf94493b8b894516240812")
                location.weather = weather  
            
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
    return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)


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
