from django.urls import path
from .views import ReminderListView, ReminderCreateView, ReminderDeleteView, ReminderUpdateView
from . import views

urlpatterns = [
    path('', ReminderListView.as_view(), name='reminder-list'),
    path('create/', ReminderCreateView.as_view(), name='reminder-create'),
    path('update/<int:pk>/', ReminderUpdateView.as_view(), name='reminder-update'),
    path('delete/<int:pk>/', ReminderDeleteView.as_view(), name='reminder-delete'),
    path('toggle-save/<str:object_type>/<int:object_id>/', views.toggle_save, name='toggle-save'),

]
