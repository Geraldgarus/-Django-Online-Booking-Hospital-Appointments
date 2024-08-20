from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Doctor, Patient
from .models import Appointment, AddDoctor, Attend
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Manager

#registration form
class DoctorRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'DOCTOR'
        if commit:
            user.save()
            Doctor.objects.create(user=user, first_name='', last_name='')
        return user

class PatientRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'PATIENT'
        if commit:
            user.save()
            Patient.objects.create(user=user, first_name='', last_name='')
        return user

class CustomAuthenticationForm(AuthenticationForm):
    pass


class ManagerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'MANAGER'
        if commit:
            user.save()
            # Create a Manager instance for the newly created user
            Manager.objects.create(user=user, first_name='', last_name='')
        return user






class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['first_name', 'last_name', 'description']

class AddDoctorForm(forms.ModelForm):
    class Meta:
        model = AddDoctor
        fields = ['first_name', 'last_name', 'specialist']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialist': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class AttendForm(forms.ModelForm):
    class Meta:
        model = Attend
        fields = ['first_name', 'last_name', 'description', 'cost', 'doctor', 'appointment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'cost': forms.NumberInput(attrs={'step': '0.01'}),
        }

#update
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['first_name', 'last_name', 'description']
        
#add form
class AddDoctorForm(forms.ModelForm):
    class Meta:
        model = AddDoctor
        fields = ['first_name', 'last_name', 'specialist']  # 
        
        
#patient apppointments

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['first_name', 'last_name', 'description']