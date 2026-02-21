from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Image

class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'phone']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['user_notes', 'image']