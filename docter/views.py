from django.shortcuts import get_object_or_404, render,redirect
from . import urls
from app1.models import Docter,Profile,Patient
from patient.models import appointment as Appointment
from .models import Availability,MedicalRecord
from django.contrib import messages

from datetime import date
from django.shortcuts import render, get_object_or_404
# Create your views here.


def docter_Dash(request):
    doctor = Docter.objects.get(profile__user=request.user)
    appointment=Appointment.objects.filter(docter=doctor)
    Patients = Patient.objects.all()
    Patient_count  = Patients.count()

    appointment_count = appointment.count()

    return render(request,'docter_dashboard.html',{"appointment":appointment,"appointment_count":appointment_count,"patient_count":Patient_count})


def approve(request,id):
    docter=Docter.objects.get(profile__user=request.user)
    app=get_object_or_404(Appointment,id=id,docter=docter)

    app.status = "Approved"
    app.save()

    messages.success(request,"appointment succesfully")

    return redirect("/docter_dash/")

def reject_appointment(request, id):

    doctor = Docter.objects.get(
        profile__user=request.user
    )

    app = get_object_or_404(
        Appointment,
        id=id,
        docter=doctor
    )

    app.status = "Rejected"
    app.save()

    return redirect("/docter_dash/")



from datetime import date
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator


def appointments(request):

    # Logged-in doctor
    doctor = get_object_or_404(
        Docter,
        profile__user=request.user
    )

    # Get appointments for this doctor
    appointments = Appointment.objects.filter(
        docter=doctor
    ).select_related(
        "patient",
        "appointment"
    ).order_by("-id")


    # =========================
    # PAGINATION
    # =========================

    paginator = Paginator(appointments, 3)

    page_number = request.GET.get("page")

    appointments_page = paginator.get_page(page_number)


    # =========================
    # UNIQUE PATIENTS
    # =========================

    patients = []
    patient_ids = set()

    for app in appointments:

        if app.patient_id not in patient_ids:

            patient = app.patient

            # Calculate age
            if patient.dob:

                today = date.today()

                patient.age = (
                    today.year
                    - patient.dob.year
                    - (
                        (today.month, today.day)
                        < (patient.dob.month, patient.dob.day)
                    )
                )

            else:

                patient.age = ""

            patients.append(patient)

            patient_ids.add(app.patient_id)


    # =========================
    # CONTEXT
    # =========================

    context = {
        "appointments": appointments_page,
        "patients": patients,
    }

    return render(
        request,
        "appointments.html",
        context
    )




def docter_request(req):
    return render (req,"request.html")

def avilable_timming(request):
    if request.method == "POST":

        day = request.POST.get("day")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        duration = request.POST.get("duration")
        fee = request.POST.get("fee")
        status = request.POST.get("status")

        Availability.objects.create(

            doctor=request.user,

            day=day,

            start_time=start_time,

            end_time=end_time,

            duration=duration,

            fee=fee,

            status=status

        )

        return redirect("/available_timming/")

    availability_list = Availability.objects.filter(
        doctor=request.user
    )

    context = {
        "availability_list": availability_list
    }

    return render(
        request,
        "avilable_timming.html",
        context
    )

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
    profile = Profile.objects.get(user=request.user)

    doctor ,created = Docter.objects.get_or_create(profile=profile)

    if request.method == "POST":

        doctor.first_name = request.POST.get("first_name")
        doctor.last_name = request.POST.get("last_name")
        doctor.display_name = request.POST.get("display_name")
        doctor.specalist = request.POST.get("designation")
        doctor.phone = request.POST.get("phone")
        doctor.email = request.POST.get("email")
        doctor.languages = request.POST.get("languages")
        doctor.membership_title = request.POST.get("membership_title")
        doctor.membership_about = request.POST.get("membership_about")

        if request.FILES.get("profile_image"):
            doctor.profile_image = request.FILES.get("profile_image")

        doctor.save()

        return redirect("/docter_profile_settings/")

    return render(request, "docter_profile_settings.html", {"doctor": doctor})    


def docter_specialties(request):
    return render(request, 'docter_speclities.html')

def invoice(request):
    return render(request, 'invoice.html')

def my_patients(request):

    # Get currently logged-in doctor
    doctor = Docter.objects.get(profile__user=request.user)

    # Get appointments belonging to this doctor
    appointments = Appointment.objects.filter(
        docter=doctor
    ).select_related("patient")

    # Get unique patients
    patients = []
    patient_ids = set()

    for app in appointments:
        if app.patient_id not in patient_ids:
            patients.append(app.patient)
            patient_ids.add(app.patient_id)

    return render(request, "my_patients.html", {
        "patients": patients,
    })

def request_page(request):

    appointment = Appointment.objects.all()






    return render(request, 'request.html',{"appointment":appointment})

def review(request):
    return render(request, 'review.html')



from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def docter_change_password(request):

    if request.method == "POST":

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check old password
        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return render(request, "docter_change_password.html")

        # Check new and confirm password
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return render(request, "docter_change_password.html")

      

        # Set new password
        request.user.set_password(new_password)
        request.user.save()

        # Keep doctor logged in
        update_session_auth_hash(request, request.user)

        messages.success(request, "Password changed successfully.")

        return redirect("docter_change_password")

    return render(request, "docter_change_password.html")


def add_medical_record(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    doctor = get_object_or_404(
        Docter,
        profile=profile
    )

    if request.method == "POST":

        record_name = request.POST.get("record_name")
        record_date = request.POST.get("record_date")
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        comments = request.POST.get("comments")
        report = request.FILES.get("report")

        MedicalRecord.objects.create(
            patient=patient,
            doctor=doctor,
            record_name=record_name,
            record_date=record_date,
            diagnosis=diagnosis,
            treatment=treatment,
            comments=comments,
            report=report
        )

        return redirect("my_patients")

    return render(
        request,
        "add_medical_record.html",
        {
            "patient": patient
        }
    )




def start_video_call(request, id):

    # Logged-in doctor
    doctor = get_object_or_404(
        Docter,
        profile__user=request.user
    )

    # Get this doctor's appointment
    appointment = get_object_or_404(
        Appointment,
        id=id,
        docter=doctor
    )

    # Only approved appointments can start
    # the video session
    if appointment.status != "Approved":
        return render(
            request,
            "video_error.html",
            {
                "message": "This appointment is not approved."
            }
        )

    # Create a unique room name
    room_name = f"docure-appointment-{appointment.id}"

    return render(
        request,
        "video_call.html",
        {
            "appointment": appointment,
            "room_name": room_name,
        }
    )