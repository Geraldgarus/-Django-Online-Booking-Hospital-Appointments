# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import DoctorRegistrationForm, PatientRegistrationForm, CustomAuthenticationForm

from .models import  Doctor, Patient

from django.contrib import messages
from .forms import AppointmentForm, AttendForm
from .models import AddDoctor123
from .models import Attend
from .models import Appointment
from django.views.generic import TemplateView
from django.contrib.auth import login as auth_login
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect


from .models import Patient
from django.contrib.auth import login as auth_login
from django.views.generic import ListView
from .models import Appointment
from django.urls import reverse_lazy
from django.views.generic.edit import  DeleteView
from .forms import ManagerRegistrationForm

from django.http import JsonResponse

@login_required(login_url="/login/")
def index1(request):
    return render(request,'index1.html')

    

@login_required(login_url="login2/")
def index2(request):
    return render(request, 'index2.html')

def index(request):
    return render(request,'index.html')


def index3(request):
    return render(request,'index3.html')




@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('index/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    
#login



def doctor_list(request):
    doctors = Doctor.objects.all()  # Retrieve all doctor records
    return render(request, 'doctor_list.html', {'doctors': doctors})


def add_doctor(request, doctor_id):
    # Placeholder logic for adding a doctor
    return redirect('doctor_list')


#delete
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect('doctor_list')



#manager dashboard
def manager_dashboard(request):
    return render(request,'manager_dashboard.html')


#doctor dashboard

def doctor_dashboard(request):
    return render(request,'doctor_dashboard.html')

#patient_dashboard

def patient_dashboard(request):
    return render(request,'patient_dashboard.html')


#logout

def logout1(request):
    
    return redirect('index') 

#
#appointment form

@login_required  # Ensure that only authenticated users can create appointments
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Create a new appointment instance but don't save it yet
            appointment = form.save(commit=False)
            # Set the user field to the currently authenticated user
            appointment.user = request.user
            # Save the appointment instance to the database
            appointment.save()
            return redirect('patient_appointments')  # Redirect to a page showing the list of appointments or another relevant page
    else:
        form = AppointmentForm()
    
    return render(request, 'create_appointment.html', {'form': form})

#ad doctor

#retrieve doctors details

def doctor_details(request):
    # Query all AddDoctor objects from the database
    doctors = AddDoctor.objects.all()
    # Pass the queryset to the template
    return render(request, 'doctor_details.html', {'doctors': doctors})

#attend form

def attend_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctor = request.user  # Assuming the authenticated user is a doctor

    if request.method == 'POST':
        form = AttendForm(request.POST)
        if form.is_valid():
            attend = form.save(commit=False)
            attend.appointment = appointment
            attend.doctor = doctor  # Set the authenticated user as the doctor
            attend.save()
            return redirect('Appointment_details')  # Redirect to a list or success page
    else:
        # Initialize the form with empty data
        form = AttendForm()
    
    context = {
        'appointment': appointment,
        'form': form,
        'doctor': doctor 
    }
    return render(request, 'attend_detail.html', context)

#attend_list
def attend_list(request):
    attends = Attend.objects.all()
    return render(request, 'attend_list.html', {'attends': attends})

def attend_list_m(request):
    attends = Attend.objects.all()
    return render(request, 'attend_list_m.html', {'attends': attends})


def dashboard(request):
    return render(request,'dashboard.html')

#appointments
def Appointment_details(request):
    # Query all AddDoctor objects from the database
    Appointments = Appointment.objects.all()
    # Pass the queryset to the template
    return render(request, 'Appointment_details.html', {'Appointments': Appointments})

def Appointment_details_p(request):
    Appointments = Appointment.objects.all()
    return render(request, 'Appointment_details_p.html', {'Appointments': Appointments})
    
    
#about
def about(request):
    return render(request, 'about.html')

#appointment list
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments_lists.html'
    context_object_name = 'appointments'

    
#update and delete


class AppointmentDeleteView(DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment-list')
    template_name = 'appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment_list')
    

def appointments_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {
        'appointment': appointment
    }
    return render(request, 'appointments_details.html', context)



class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment_lists.html'
    context_object_name = 'appointments'


#total
class index1View(TemplateView):
    template_name = 'index1.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_appointments'] = Appointment.objects.count()  # Get total count
        context['total_attends'] = Attend.objects.count() 
        context['total_doctors'] = Doctor.objects.count()  # Get total doctors count
        context['total_patients'] = Patient.objects.count()  # Get total patients count
        return context
    
    
class index3View(TemplateView):
    template_name = 'index3.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_appointments'] = Appointment.objects.count()  # Get total appointments count
        context['total_attends'] = Attend.objects.count()  # Get total attendances count
        context['total_patients'] = Patient.objects.count()  # Get total patients count
        return context
    


class Index2View(TemplateView):
    template_name = 'index2.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_done_appointments'] = Appointment.objects.count()  # Get total done appointments
        context['total_doctors'] = AddDoctor123.objects.count()  # Get total doctors count from AddDoctor123
        return context
#registration forms


def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You may now login.')
            return redirect('login2')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'register_doctor.html', {'form': form})


def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login2')
    else:
        form = PatientRegistrationForm()
    return render(request, 'register_patient.html', {'form': form})


def register_manager(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login2')  # Redirect to the login page or any other page you want
    else:
        form = ManagerRegistrationForm()
    return render(request, 'register_manager.html', {'form': form})

def login2(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirect based on user type
            if user.user_type == 'DOCTOR':
                return redirect('index3')  # Redirect to the doctor-specific page
            elif user.user_type == 'PATIENT':
                return redirect('index2')  # Redirect to the patient-specific page
            elif user.user_type == 'MANAGER':
                return redirect('index1')  # Redirect to the manager-specific page
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login2.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')

#update appointment

@login_required  # Ensure that only authenticated users can update appointments
def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            # Ensure the user field is set to the currently authenticated user
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('appointment_lists')  # Redirect to the list after saving
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'appointment_form.html', {'form': form, 'appointment': appointment})


#delete appointmwnt
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
    return redirect('appointment_lists')


#update attend_list_m

def update_attend1(request, pk):
    """
    View to handle updating an attendance record.
    """
    # Fetch the specific Attend record or return 404 if not found
    attend = get_object_or_404(Attend, pk=pk)
    
    if request.method == 'POST':
        # Create a form instance with the POST data and the current record instance
        form = AttendForm(request.POST, instance=attend)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance record updated successfully.')
            return redirect('attend_list_m')  # Redirect to the attend list page
    else:
        # Create a form instance with the current record instance
        form = AttendForm(instance=attend)
    
    # Render the form template
    return render(request, 'attend_form.html', {'form': form})
#delete attend_lists_m


def delete_attend1(request, pk):
    """
    View to handle the deletion of an attendance record.
    """
    if request.method == 'POST':
        attend = get_object_or_404(Attend, pk=pk)
        attend.delete()
        messages.success(request, 'Attendance record deleted successfully.')
        return redirect('attend_list_m')  # Redirect to the attend list page

    # If not a POST request, redirect to the attend list page
    return redirect('attend_list_m')
#doctor appointments


def patient_doctor_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'patient_doctor_appointment.html', {'appointment': appointment})



def patient_appointments(request):
    # Retrieve all appointments or filter as needed
    appointments = Appointment.objects.all()  # Adjust filtering as needed
    
    return render(request, 'patient_appointments.html', {'appointments': appointments})


#delete and update patient apppointments

def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('patient_appointments')  # Redirect to the appointments list
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'appointment_update.html', {'form': form, 'appointment': appointment})



def appointment_delete(request, pk):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        return redirect('patient_appointments')  # Redirect to the appointments list\
            
            
#doctor atteded
def update_attend(request, id):
    # Fetch the Attend object by its ID
    attend = get_object_or_404(Attend, id=id)

    if request.method == 'POST':
        form = AttendForm(request.POST, instance=attend)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attend record updated successfully.')
            return redirect('attend_list')  # Redirect to the list view or wherever you want
    else:
        form = AttendForm(instance=attend)

    return render(request, 'update_attend.html', {'form': form})

def delete_attend(request, pk):
    """
    View to handle the deletion of an attendance record.
    """
    if request.method == 'POST':
        # Get the attendance record to delete
        attend = get_object_or_404(Attend, pk=pk)
        
        # Delete the attendance record
        attend.delete()
        
        # Provide a success message
        messages.success(request, 'Attendance record deleted successfully.')
        
        # Redirect to the attend list page
        return redirect('attend_list')
    
    # If the request method is not POST, redirect to the attend list page
    return redirect('attend_list')


#profile_patient
def profile_p(request):
    return render(request, 'profile_p.html')

#profile doctor
def profile_d(request):
    return render(request, 'profile_d.html')

#notifications

#add doctor

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddDoctor123Form
from .models import AddDoctor123

@login_required
def create_adddoctor123(request):
    if request.method == "POST":
        form = AddDoctor123Form(request.POST)
        if form.is_valid():
            # Create a new AddDoctor123 record with the authenticated user
            adddoctor123_instance = form.save(commit=False)
            adddoctor123_instance.doctor = request.user  # Set the authenticated user
            adddoctor123_instance.save()
            return redirect('index3')  # Redirect to a success page or another view
    else:
        form = AddDoctor123Form()

    return render(request, 'create_adddoctor123.html', {'form': form})

#doctor details123
from django.shortcuts import render
from .models import AddDoctor123

def doctor_details123(request):
    # Fetch all records from AddDoctor123
    doctor_records = AddDoctor123.objects.all()
    
    # Render the template with the fetched records
    return render(request, 'doctordetails123.html', {'doctor_records': doctor_records})




