# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

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
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        default=1  # Replace with a valid user ID if applicable
    )
    description = models.TextField()
    date = models.DateField()  # New date field

    def __str__(self):
        # Use the user's first and last name directly
        return f"Appointment for {self.user.first_name} {self.user.last_name} on {self.date}"
   
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Attend(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Links to the CustomUser model
    comment = models.TextField(blank=True, null=True)  # Optional comments
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # Cost of attendance
    date = models.DateField(default=timezone.now)  # Default to current date

    def __str__(self):
        return f'{self.doctor.username} attended {self.appointment} on {self.date}'




#adddoctor

class AddDoctor123(models.Model):
    specialist = models.TextField()
    date = models.DateField()
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Record by Dr. {self.doctor.first_name} {self.doctor.last_name} on {self.date}"