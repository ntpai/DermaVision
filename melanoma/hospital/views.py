from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, "hospital/index.html")

def signin(request):
    return render(request, "hospital/signin.html")

def signup(request):
    return render(request, "hospital/signup.html")

@login_required
def log_out(request):
    logout(request)
    return redirect('user_home')