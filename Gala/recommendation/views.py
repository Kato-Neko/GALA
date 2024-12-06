from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Location
from .forms import LocationForm
from django.views.generic import ListView
from .utils import get_address_from_coordinates

class LocationHomeView(ListView):
    model = Location
    template_name = 'home.html'  # Update to your home page template
    context_object_name = 'locations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add locations as JSON-like data to the context
        locations = Location.objects.all()
        locations_data = [
            {
                "id": location.id,
                "name": location.name,
                "description": location.description,
                "longitude": location.longitude,
                "latitude": location.latitude,
                "weather": location.weather,
                "image_url": location.image.url if location.image else None,
            }
            for location in locations
        ]
        
        context['locations'] = locations_data  # This can be used in JavaScript
        return context

def admin_location_view(request):
    locations = Location.objects.all()
    return render(request, 'admin_location.html', {'locations': locations})

def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            location = form.save(commit=False)
            
            # Fetch address from coordinates
            if location.latitude and location.longitude:
                api_key = "ge-ea5a9c6688e4ac48"  # Replace with your actual API key
                location.address = get_address_from_coordinates(location.latitude, location.longitude, api_key)
            
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
                    'address': location.address,  # Include address
                }
            })
    return JsonResponse({'status': 'error', 'message': 'Invalid data'})


def edit_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES, instance=location)  # Include request.FILES
        if form.is_valid():
            location = form.save(commit=False)

            # Fetch a new address if coordinates are updated
            if location.latitude and location.longitude:
                api_key = "ge-ea5a9c6688e4ac48"  # Replace with your actual API key
                location.address = get_address_from_coordinates(location.latitude, location.longitude, api_key)
            
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
                    'address': location.address,  # Include address
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
