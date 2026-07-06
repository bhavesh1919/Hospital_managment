from django.shortcuts import render
from . import urls

# Create your views here.


def docter_Dash(req):
    return render(req,'docter_dashboard.html')

# def docter_Dash(req):
#     return render(req,'docter_dashboard.html')

def Appointment(req):
    return render(req,"appointments.html")

def docter_request(req):
    return render (req,"request.html")

def avilable_timming(req):
    return render(req,"avilable_timming.html")


def account(request):
    return render(request, 'account.html')

def chat(request):
    return render(request, 'chat.html')

def docter_blog(request):
    return render(request, 'docter_blog.html')

def docter_change_password(request):
    return render(request, 'docter_change_password.html')

def docter_dashboard(request):
    return render(request, 'docter_dashboard.html')

def docter_payment(request):
    return render(request, 'docter_payment.html')

def docter_profile_settings(request):
    return render(request, 'docter_profile_settings.html')

def docter_specialties(request):
    return render(request, 'docter_speclities.html')

def invoice(request):
    return render(request, 'invoice.html')

def my_patients(request):
    return render(request, 'my_patients.html')

def request_page(request):
    return render(request, 'request.html')

def review(request):
    return render(request, 'review.html')