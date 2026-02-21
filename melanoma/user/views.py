from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *

def index(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        print(f"ID: {user_id}")
    return render(request, 'users/index.html')

def signup(request):
    if request.method == 'POST':
        user_form = UserSignupForm(request.POST)
        profile_form = PatientProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save()
            
            profile = profile_form.save(commit=False)
            
            profile.user = user  # This fills the OneToOneField
            
            profile.save()
            
            login(request, user)
            return redirect('index')
    else: 
        user_form = UserSignupForm()
        profile_form = PatientProfileForm()
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/users')

        else:
            messages.error(request, "Invalid username or password!")
            return redirect("users/signin.html")
    return render(request, "users/signin.html")

@login_required
def log_out(request):
    logout(request)
    return redirect('user_home')

@login_required
def upload_image(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            image_instance.user = request.user
            image_instance.save()
            return redirect('user_home')
    else:
        form = UploadImageForm()
    return render(request, 'users/upload_image.html', {'form':form})