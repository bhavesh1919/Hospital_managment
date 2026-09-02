from django.shortcuts import render


# Create your views here.
def admindashboard(request):
    return render(request,"admin_dash55.html")


def appointment_list(request):
    return render(request,"appointment_list.html")


def doctor_list(request):
    return render(request, "doctor_list.html")


def patient_list(request):
    return render(request, "patient.html")


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