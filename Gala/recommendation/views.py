from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Location
from .forms import LocationForm

def admin_location_view(request):
    locations = Location.objects.all()
    form = LocationForm()
    return render(request, 'admin_location.html', {'locations': locations, 'form': form})

def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save()
            return JsonResponse({
                'status': 'success',
                'location': {
                    'id': location.id,
                    'name': location.name,
                    'description': location.description,
                    'longitude': location.longitude,
                    'latitude': location.latitude,
                    'weather': location.weather,
                }
            })
    return JsonResponse({'status': 'error'}, status=400)

def edit_location(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save()
            return JsonResponse({
                'status': 'success',
                'location': {
                    'id': location.id,
                    'name': location.name,
                    'description': location.description,
                    'longitude': location.longitude,
                    'latitude': location.latitude,
                    'weather': location.weather,
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