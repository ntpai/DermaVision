import datetime
from datetime import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Gender(models.TextChoices):
    Male = 'M', 'Male'
    Female = 'F', 'Female'
    PREFER_NOT_TO_SAY = 'U', 'Prefer not to say'

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=1,
        choices=Gender,
        default=Gender.PREFER_NOT_TO_SAY,
        help_text="Select your gender."
    )
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"username:{self.user.username} gender: {self.get_gender_display()}"

def upload_to(instance, image_name):
    return f"images/{image_name}"

class Image(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    user_notes = models.CharField(max_length=250)
    image = models.ImageField(upload_to=upload_to,blank=True, null=True)