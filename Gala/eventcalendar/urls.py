from django.urls import path
from .views import ReminderListView, ReminderCreateView, ReminderDeleteView, ReminderUpdateView

urlpatterns = [
    path('', ReminderListView.as_view(), name='reminder-list'),
    path('create/', ReminderCreateView.as_view(), name='reminder-create'),
    path('update/<int:pk>/', ReminderUpdateView.as_view(), name='reminder-update'),  # Add this
    path('delete/<int:pk>/', ReminderDeleteView.as_view(), name='reminder-delete'),
]
