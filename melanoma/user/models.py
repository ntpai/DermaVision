from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
        

class Image(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    upload_at = models.DateTimeField()
    user_notes = models.TextField()

class Hospital(models.Model):
    hospital_name = models.CharField(max_length=100)
    address = models.TextField()
    contact_email = models.EmailField(max_length=254)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
class Appointments(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return f"{self.patient_id} visiting {self.doctor_id} at {self.time} on {self.date}"
    
