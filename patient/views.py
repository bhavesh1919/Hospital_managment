from django.shortcuts import render,redirect,get_object_or_404
from . import urls
from app1.models import Patient,Profile,Docter
from docter.models import Availability,MedicalRecord
from .models import appointment,Vital,Favourite
from datetime import datetime
from django.contrib import messages 
from django.db.models import Case, When, IntegerField
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from django.db.models import Case, When, IntegerField

@login_required(login_url="/login/")


def patient_dashboard(req):

    patient = Patient.objects.get(profile__user=req.user)

    # Get appointments
    appointments_qs = appointment.objects.filter(
        patient=patient,
        status__in=["Pending", "Approved"]
    ).select_related(
        "docter"
    ).order_by(
        Case(
            When(status="Approved", then=0),
            When(status="Pending", then=1),
            output_field=IntegerField(),
        )
    )

    # Use Indian Standard Time explicitly
    india_timezone = ZoneInfo("Asia/Kolkata")

    now = datetime.now(india_timezone).replace(tzinfo=None)

    # Convert to a list so each appointment can receive
    # its call_available attribute
    av = list(appointments_qs)

    for app in av:

        # Hide the button unless all conditions are satisfied
        app.call_available = False

        if (
            app.status == "Approved"
            and app.appointment_date
            and app.appointment_time
        ):

            appointment_start = datetime.combine(
                app.appointment_date,
                app.appointment_time
            )

            appointment_end = appointment_start + timedelta(hours=2)

            # Button is visible from the appointment start
            # until exactly two hours after it starts
            app.call_available = (
                appointment_start <= now < appointment_end
            )

            # Debug output in the Django terminal
            print(
                f"[VIDEO DEBUG] Appointment #{app.id} | "
                f"Status={app.status} | "
                f"Start={appointment_start} | "
                f"End={appointment_end} | "
                f"Now={now} | "
                f"Available={app.call_available}"
            )

    # Keep health records unchanged
    health_record = Vital.objects.filter(
        patient_id=patient.id
    ).order_by("-added_on").first()

    # Keep favourites unchanged
    favourites = Favourite.objects.filter(
        patient=patient
    ).select_related("docter")

    return render(
        req,
        "patient_dashboard.html",
        {
            "av": av,
           "health_record": health_record,
            "favourites": favourites,
        }
    )



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
    profile = Profile.objects.get(user=request.user)
    patient = Patient.objects.get(profile=profile)

    records = MedicalRecord.objects.filter(
        patient=patient
    ).select_related('doctor').order_by('-record_date')

    return render(request, 'medical_record.html', {
        'records': records
    })

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
    docters = Docter.objects.all()
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
    p = Patient.objects.filter(profile=profile)

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

    
    doctor_obj = get_object_or_404(
        Docter,
        profile__user=slot.doctor
    )

    if request.method == "POST":

        selected_date = request.POST.get("appointment_date")

       
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


def patient_video_call(request, id):

    patient = get_object_or_404(
        Patient,
        profile__user=request.user
    )

    Appointment = get_object_or_404(
        appointment,
        id=id,
        patient=patient
    )

    if Appointment.status != "Approved":
        return render(
            request,
            "video_error.html",
            {
                "message": "This appointment is not approved."
            }
        )

    room_name = f"docure-appointment-{Appointment.id}"

    return render(
        request,
        "video_call.html",
        {
            "appointment": Appointment,
            "room_name": room_name,
        }
    )

from django.contrib.auth import logout
from django.shortcuts import redirect

def Logout(request):
    logout(request)
    return redirect('login')


from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

@login_required
def password_change(request):

    if request.method == "POST":

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check old password
        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect("password_change")

        # Check new password and confirm password
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect("password_change")

        # Change password
        request.user.set_password(new_password)
        request.user.save()

        # Keep user logged in
        update_session_auth_hash(request, request.user)

        messages.success(request, "Password changed successfully.")

        return redirect("password_change")

    return render(request, "password_change.html")