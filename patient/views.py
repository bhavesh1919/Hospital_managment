from django.shortcuts import render,redirect,get_object_or_404
from . import urls
from app1.models import Patient,Profile,Docter
from docter.models import Availability
from .models import appointment,Vital,Favourite
from datetime import datetime
from django.contrib import messages 
from django.db.models import Case, When, IntegerField

# Create your views here.

def patient_dashboard(req):
    doctors = Docter.objects.all()
    patient=Patient.objects.get(profile__user=req.user)

    # av = appointment.objects.all()
    # availability = Availability.objects.filter(
    #         status="Available"
    #     ).select_related("doctor")


    av = appointment.objects.filter(
    patient=patient,
    status__in=["Pending", "Approved"]
    ).select_related('docter').order_by(
        Case(
            When(status="Approved",then=0),
            When(status="Pending", then=1),
            output_field=IntegerField(),
        )
    )

    health_record = Vital.objects.filter(
        patient=patient
    ).order_by("-id").first()

       
    

    # Get only this patient's favourite doctors
    favourites = Favourite.objects.filter(
        patient=patient
    ).select_related("docter")


    


    return render(req,"patient_dashboard.html",{"av":av,"health_record": health_record,"favourites": favourites,})



def cancel_appointment(request, id):

    patient = Patient.objects.get(
        profile__user=request.user
    )

    app = get_object_or_404(
        appointment,
        id=id,
        patient=patient
    )

    if app.status in ["Pending", "Approved"]:
        app.status = "Cancelled"
        app.save()

    return redirect("/patient/")

def patients_appointment(request):
    doctors = Docter.objects.all()
   
    # appoinent = appointment.objects.filter(patient=Patient)
    availability = Availability.objects.filter(
        status="Available"
    ).select_related("doctor")

    return render(request, 'patients_appointment.html',{"availability": availability})


def patient_account(request):
    return render(request, 'patient_Account.html')


def patient_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        profile_photo = request.FILES.get("img")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        blood = request.POST.get("blood")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        dob = request.POST.get("dob")
        

        if dob:
            dob = datetime.strptime(dob, "%d/%m/%Y").date()

  

        patient, created = Patient.objects.get_or_create(profile=profile)

        patient.profile_photo = profile_photo
        patient.fname = fname
        patient.lname = lname
        patient.dob = dob
        patient.phone = phone
        patient.gender = gender
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

    patient = Patient.objects.get(profile__user=request.user)

    vitals = Vital.objects.filter(patient=patient)




    return render(request, 'medical_details.html', {
            "vitals": vitals
        })


def add_vital(request,patient_id):

    patient = Patient.objects.get(profile__user_id=patient_id)

    if request.method == "POST":

        Vital.objects.create(
            patient=patient,
            
            blood_pressure=request.POST.get("blood_pressure"),
            heart_rate=request.POST.get("heart_rate"),
            glucose_level=request.POST.get("glucose_level"),
            body_temperature=request.POST.get("body_temperature"),
            bmi=request.POST.get("bmi"),
            spo2=request.POST.get("spo2"),
            weight=request.POST.get("weight"),
            fbc_status=request.POST.get("fbc_status"),
        )

        return redirect("medical_details")

    return render(request, "add_vital.html")


def favourites(request):

    patient = Patient.objects.get(
        profile__user=request.user
    )

    # Show ALL doctors
    docters = Docter.objects.all()

    # Get favourite doctor IDs of current patient
    favourite_ids = Favourite.objects.filter(
        patient=patient
    ).values_list("docter_id", flat=True)

    return render(request, "favourites.html", {
        "docters": docters,
        "favourite_ids": favourite_ids,
    })

def dependent(request):
    return render(request, 'dependent.html')

def add_favourite(request, doctor_id):

    patient = Patient.objects.get(
        profile__user=request.user
    )

    doctor = get_object_or_404(
        Docter,
        id=doctor_id
    )

    Favourite.objects.get_or_create(
        patient=patient,
        docter=doctor
    )

    return redirect("favourites")




def sidear(request):

    
    profile = Profile.objects.get(user=request.user)
    p = Patient.objects.filter(profile=profile).first()


    return render(request,"sidebar.html" ,{"p":p})
def book_appointment(request, id):

    # Get selected availability slot
    slot = get_object_or_404(
        Availability,
        id=id,
        status="Available"
    )

    # Get logged-in patient
    patient = get_object_or_404(
        Patient,
        profile__user=request.user
    )

    # Get doctor from availability
    doctor_obj = get_object_or_404(
        Docter,
        profile__user=slot.doctor
    )

    if request.method == "POST":

        selected_date = request.POST.get("appointment_date")

        # Date is required
        if not selected_date:
            messages.error(
                request,
                "Please select an appointment date."
            )

            return render(
                request,
                "book_appointment.html",
                {
                    "slot": slot
                }
            )

        # Convert HTML date to Python date
        try:
            appointment_date = datetime.strptime(
                selected_date,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            messages.error(
                request,
                "Invalid appointment date."
            )

            return render(
                request,
                "book_appointment.html",
                {
                    "slot": slot
                }
            )

        # Check that selected date is the same day
        # as the Availability day
        if appointment_date.strftime("%A") != slot.day:
            messages.error(
                request,
                f"Please select a {slot.day}."
            )

            return render(
                request,
                "book_appointment.html",
                {
                    "slot": slot
                }
            )

        # Prevent booking the same doctor/time/date twice
        already_booked = appointment.objects.filter(
            docter=doctor_obj,
            appointment_date=appointment_date,
            appointment_time=slot.start_time,
            status__in=["Pending", "Approved"]
        ).exists()

        if already_booked:
            messages.error(
                request,
                "This time slot is already booked."
            )

            return render(
                request,
                "book_appointment.html",
                {
                    "slot": slot
                }
            )

        # Create appointment
        appointment.objects.create(
            patient=patient,
            docter=doctor_obj,
            appointment=slot,
            appointment_day=slot.day,
            appointment_date=appointment_date,
            appointment_time=slot.start_time,
            status="Pending"
        )

        messages.success(
            request,
            "Appointment booked successfully."
        )

        return redirect("/patient/")

    return render(
        request,
        "book_appointment.html",
        {
            "slot": slot
        }
    )