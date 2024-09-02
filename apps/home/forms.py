from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Doctor, Patient
from .models import Appointment, Attend
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Manager
from .models import AddDoctor123
#registration form

class DoctorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    username = forms.CharField(max_length=150, required=True, label='Username')
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'DOCTOR'
        if commit:
            user.save()
            Doctor.objects.create(
                user=user, 
                first_name=self.cleaned_data['first_name'], 
                last_name=self.cleaned_data['last_name']
            )
        return user

class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    username = forms.CharField(max_length=150, required=True, label='Username')
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'PATIENT'
        if commit:
            user.save()
            Patient.objects.create(
                user=user, 
                first_name=self.cleaned_data['first_name'], 
                last_name=self.cleaned_data['last_name']
            )
        return user

class CustomAuthenticationForm(AuthenticationForm):
    pass

class ManagerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    username = forms.CharField(max_length=150, required=True, label='Username')
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'MANAGER'
        if commit:
            user.save()
            Manager.objects.create(
                user=user, 
                first_name=self.cleaned_data['first_name'], 
                last_name=self.cleaned_data['last_name']
            )
        return user



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['description', 'date']  # Only include the fields you need
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})  # This ensures a date picker is used
        }


#adddoctor form


class AttendForm(forms.ModelForm):
    class Meta:
        model = Attend
        fields = ['comment', 'cost', 'date']  # Include fields you want in the form
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Use a date picker for the date field
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Customize the comment textarea
            'cost': forms.NumberInput(attrs={'step': '0.01'})  # Allow decimal values for cost
        }
        labels = {
            'comment': 'Comment',
            'cost': 'Cost',
            'date': 'Date of Attendance'
        }
#add doctor 

class AddDoctor123Form(forms.ModelForm):
    class Meta:
        model = AddDoctor123
        fields = ['specialist', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

