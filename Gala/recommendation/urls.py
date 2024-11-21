# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommendation_view, name='recommendation'),
    path('admin-location/', views.admin_location_view, name='admin_location'),
    path('add-location/', views.add_location, name='add_location'),
    path('edit-location/<int:pk>/', views.edit_location, name='edit_location'),
    path('delete-location/<int:pk>/', views.delete_location, name='delete_location'),
]