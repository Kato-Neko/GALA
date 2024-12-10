# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.recommendation_view, name='recommendation'),
    path('admin-location/', views.admin_location_view, name='admin_location'),
    path('add-location/', views.add_location, name='add_location'),
    path('edit-location/<int:pk>/', views.edit_location, name='edit_location'),
    path('delete-location/<int:pk>/', views.delete_location, name='delete_location'),
    path('toggle-save/<str:object_type>/<int:object_id>/', views.toggle_save, name='toggle-save'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)