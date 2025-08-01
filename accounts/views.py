from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

# Create your views here.


def register(request):
    """
    Handles user registration.
    If the request method is POST, it attempts to validate and save the
    RegisterForm. If valid, it saves the user, populates the associated
    user profile's bio and type fields, and then redirects to the 'login' page.
    If the form is invalid, it re-renders the registration page with an error.
    If the request method is GET, it displays blank.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(form.cleaned_data)
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.role = form.cleaned_data.get('role')
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def profile(request):
    """
    Renders the user's profile page.
    This view displays the 'accounts/profile.html' template.
    """
    return render(request, 'accounts/profile.html')
