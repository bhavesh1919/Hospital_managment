from django.shortcuts import render
from app1.models import Docter,Patient
from docter.models import Availability
from patient.models import appointment


from django.contrib.auth.decorators import login_required
from django.db.models import Sum



# Create your views here.
def admindashboard(request):
    doctors = Docter.objects.prefetch_related(
        "doctor_specialities__speciality"
    ).all()
    patients = Patient.objects.all()
    appointments = appointment.objects.select_related(
        "docter",
        "patient",
        "appointment",
    ).all().order_by("-created_at")

    doctor_count = doctors.count()
    patient_count = patients.count()
    appointment_count = appointments.count()

    revenue = appointments.aggregate(
        total=Sum("appointment__fee")
    )["total"] or 0

    return render(request, "admin_dash55.html", {
            "doctors": doctors,
            "patients": patients,
            "appointments": appointments,
            "doctor_count": doctor_count,
            "patient_count": patient_count,
            "appointment_count": appointment_count,
            "revenue": revenue,
        })


def appointment_list(request):
    appointments = appointment.objects.select_related(
        "docter",
        "patient",
        "appointment",
        "docter__profile__user",
        "patient__profile__user"
    ).prefetch_related(
        "docter__doctor_specialities__speciality"
    ).all().order_by("-created_at")
    return render(request, "appointment_list.html", {"appointments": appointments})


def doctor_list(request):
    doctors = Docter.objects.prefetch_related(
        "doctor_specialities__speciality",
        "profile__user"
    ).all()
    return render(request, "docter_list.html", {"doctors": doctors})


def patient_list(request):

    patient = Patient.objects.all()

    return render(request, "patient.html",{"patient":patient})


def patient_copy(request):
    return render(request, "patient copy 8.html")


def profile(request):
    return render(request, "profile.html")


def report(request):
    return render(request, "report.html")


def review(request):
    return render(request, "review1.html")


def settings(request):
    return render(request, "settings.html")


def specialities(request):
    return render(request, "specialities.html")


def transaction_list(request):
    return render(request, "transaction_list.html")




from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from docter.models import Speciality


# =========================================================
# ADMIN SPECIALITIES
# =========================================================

@login_required
def specialities(request):

    speciality_list = Speciality.objects.prefetch_related(
        "doctor_specialities__doctor"
    ).all().order_by("id")

    context = {
        "specialities": speciality_list,
    }

    return render(
        request,
        "specialities.html",
        context
    )


# =========================================================
# ADD SPECIALITY
# =========================================================

@login_required
def add_speciality(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()

        if not name:

            messages.error(
                request,
                "Please enter speciality name."
            )

            return redirect("specialities")

        if Speciality.objects.filter(
            name__iexact=name
        ).exists():

            messages.error(
                request,
                "This speciality already exists."
            )

            return redirect("specialities")

        Speciality.objects.create(
            name=name
        )

        messages.success(
            request,
            "Speciality added successfully."
        )

        return redirect("specialities")

    return redirect("specialities")


# =========================================================
# EDIT SPECIALITY
# =========================================================

@login_required
def edit_speciality(request, speciality_id):

    speciality = get_object_or_404(
        Speciality,
        id=speciality_id
    )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()

        if not name:

            messages.error(
                request,
                "Please enter speciality name."
            )

            return redirect("specialities")

        duplicate = Speciality.objects.filter(
            name__iexact=name
        ).exclude(
            id=speciality.id
        ).exists()

        if duplicate:

            messages.error(
                request,
                "This speciality already exists."
            )

            return redirect("specialities")

        speciality.name = name
        speciality.save()

        messages.success(
            request,
            "Speciality updated successfully."
        )

    return redirect("specialities")


# =========================================================
# DELETE SPECIALITY
# =========================================================

@login_required
def delete_speciality(request, speciality_id):

    speciality = get_object_or_404(
        Speciality,
        id=speciality_id
    )

    speciality.delete()

    messages.success(
        request,
        "Speciality deleted successfully."
    )

    return redirect("specialities")