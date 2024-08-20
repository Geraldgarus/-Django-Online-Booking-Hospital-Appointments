# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
        ('MANAGER', 'manager'),
        
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='PATIENT',  # Set default type if necessary
    )

    # Other fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
    )

    def __str__(self):
        return self.username

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'DOCTOR'})
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'PATIENT'})
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'MANAGER'})
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Appointment(models.Model):
    # Define the fields for the Appointment model
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return f"Appointment: {self.first_name} {self.last_name}"
    
   

class AddDoctor(models.Model):
    # Define the fields for the AddDoctor model
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    specialist = models.CharField(max_length=50)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}, Specialist: {self.specialist}"

#notification

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
class Attend(models.Model):
    # Define the fields for the Attend model
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    doctor = models.ForeignKey(AddDoctor, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attendance: {self.first_name} {self.last_name} with Dr. {self.doctor.first_name} {self.doctor.last_name}"





