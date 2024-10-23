from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    request.session.flush()  # Clear session data
    response = redirect('home')  # Replace with your home URL
    response.delete_cookie('username')  # Clear the cookie if you set it
    return response

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            request.session['username'] = username  # Store username in session
            response = redirect('home')  # Replace 'home' with your main page URL name
            response.set_cookie('username', username, max_age=3600)  # Optional: set a cookie
            return response
    return render(request, 'registration/login.html')  # Ensure this path matches your login template


@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })
