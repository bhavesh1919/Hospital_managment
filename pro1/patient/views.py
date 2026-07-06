from django.shortcuts import render
from . import urls

# Create your views here.

def patient_dashboard(req):
    return render(req,"patient_dashboard.html")


def patients_appointment(request):
    return render(request, 'patients_appointment.html')


def patient_account(request):
    return render(request, 'patient_account.html')


def patient_invoice(request):
    return render(request, 'patient_invoice.html')


def medical_record(request):
    return render(request, 'medical_record.html')


def medical_details(request):
    return render(request, 'medical_details.html')


def favourites(request):
    return render(request, 'favourites.html')


def dependent(request):
    return render(request, 'dependent.html')
