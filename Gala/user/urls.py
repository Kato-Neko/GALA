from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    # Login and signup views
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # Account management (with login required decorator)
    path('manageaccount/', views.manage_account, name='manageaccount'),
    path('delete-account/', views.delete_account, name='delete_account'),

    # You can also use Django's built-in password change views if needed
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #others
    path('search', views.search, name='search'),
    path('api/user-location', views.save_user_location, name='save_user_location'),
    path('toggle-save/<int:event_id>/', views.toggle_save, name='toggle-save'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
