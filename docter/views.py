from django.shortcuts import get_object_or_404, render,redirect
from . import urls
from app1.models import Docter,Profile
from patient.models import appointment as Appointment
from .models import Availability

# Create your views here.


def docter_Dash(request):
    doctor = Docter.objects.get(profile__user=request.user)
    appointment=Appointment.objects.filter(docter=doctor)
    return render(request,'docter_dashboard.html',{"appointment":appointment})


def approve(request,id):
    docter=Docter.objects.get(profile__user=request.user)
    app=get_object_or_404(Appointment,id=id,docter=docter)

    app.status = "Approved"
    app.save()

    return redirect("/docter_Dash/")

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

    return redirect("/docter_Dash/")



# def docter_Dash(req):
#     return render(req,'docter_dashboard.html')

def Appointment(req):
    return render(req,"appointments.html")

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
        doctor.designation = request.POST.get("designation")
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


    
    return render(request, 'my_patients.html')

def request_page(request):
    return render(request, 'request.html')

def review(request):
    return render(request, 'review.html')