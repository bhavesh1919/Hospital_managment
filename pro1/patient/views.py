from django.shortcuts import render,redirect
from . import urls
from app1.models import Patient,Profile
from datetime import datetime

# Create your views here.

def patient_dashboard(req):
    return render(req,"patient_dashboard.html")


def patients_appointment(request):
    return render(request, 'patients_appointment.html')


def patient_account(request):
    return render(request, 'patient_Account.html')


def patient_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        profile_photo = request.FILES.get("img")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        dob = request.POST.get("dob")

        if dob:
            dob = datetime.strptime(dob, "%d/%m/%Y").date()

        phone = request.POST.get("phone")
        email = request.POST.get("email")
        blood = request.POST.get("blood")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")

        patient, created = Patient.objects.get_or_create(profile=profile)

        patient.profile_photo = profile_photo
        patient.fname = fname
        patient.lname = lname
        patient.dob = dob
        patient.phone = phone
        patient.email = email
        patient.blood = blood
        patient.address = address
        patient.city = city
        patient.state = state
        patient.pincode = pincode

        patient.save()

        return redirect("patient_profile")

    p = Patient.objects.filter(profile=profile).first()

    return render(request, "patient_profile.html", {
        "p": p
    })


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
