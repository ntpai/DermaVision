from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from detection_model.predictor import predict_melanoma
from detection_model.visualizer import visualizer
from .forms import *
from .models import Image

def index(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        print(f"Login ID: {user_id}")
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
            return redirect('user_home')
    else: 
        user_form = UserSignupForm()
        profile_form = PatientProfileForm()
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/signup.html', context=context)


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("user_signin")
    return render(request, "users/signin.html")

@login_required
def log_out(request):
    logout(request)
    return redirect('user_home')

@login_required
def upload_image(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        user = get_user_model()
        patient_ref = user.objects.get(pk=request.user.id)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user_id = patient_ref
            form_instance.save()
            return redirect('user_image_result')
    else:
        form = UploadImageForm()
    return render(request, 'users/upload_image.html', {'form':form})

@login_required
def image_result(request):
    current_user_id = request.user.id
    image_path = Image.objects.filter(user_id=current_user_id).order_by('-upload_at').first()
    prediction = predict_melanoma(image_path.image.path)
    visuals = visualizer(image_path.image.path)
    """
    Prediction givens 
    label: Benign | Malignant
    probability: Probability of the result being Benign or Malignant     
    features: list of extracted values used by predictor to determine if the given image has 
            benign or malignant result
    message: Message from predictor(can contain error or success message
    """
    if prediction['label']  != "Error":
        context = {
            'is_valid': True,
            'image_path': image_path,
            'contour_image': visuals['contour_image'],
            'label': prediction['label'],
            'message': prediction['message'],
            'features': prediction['features'],
            'accuracy': prediction['probability']
        }
    else:
        context = {
            'is_valid': False,
            'message': prediction['message'],
            'label': "Error"
        }
    return render(request, 'users/image_result.html',context=context)