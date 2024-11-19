#user/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from user.models import Profile

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back, {}!'.format(user.username))
            next_url = request.POST.get('next') or request.GET.get('next') or '/home/'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below and try again.')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def account_management(request):
    user = request.user

    # Ensure the profile exists
    profile, created = Profile.objects.get_or_create(user=user)

    success = False

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        profile_picture = request.FILES.get('profile_picture')

        # Update user fields
        if username and username != user.username:
            user.username = username
        if first_name and first_name != user.first_name:
            user.first_name = first_name
        if last_name and last_name != user.last_name:
            user.last_name = last_name
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  # Keep user logged in

        user.save()

        # Update profile picture if a new one is uploaded
        if profile_picture:
            profile.profile_picture = profile_picture
            profile.save()

        success = True
        messages.success(request, "Account updated successfully!")
        return redirect('account_management')  # Stay on the same page

    return render(request, 'account_management.html', {'user': user, 'profile': profile, 'success': success})

def home(request):
    return render(request, 'home.html')