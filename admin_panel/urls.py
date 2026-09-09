
from django.urls import path
from . import views


urlpatterns = [
   
    path("admin_dash/",views.admindashboard,name="admin_dashboard"),
    
    path("appointments_list/", views.appointment_list, name="appointment_list"),
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("patients/", views.patient_list, name="patient_list"),
    path("patient-copy/", views.patient_copy, name="patient_copy"),
    path("profile/", views.profile, name="admin_profile"),
    path("reports/", views.report, name="reports"),
    path("reviews/", views.review, name="reviews"),
    path("settings/", views.settings, name="settings"),
    path("specialities/", views.specialities, name="specialities"),
    path("transactions/", views.transaction_list, name="transaction_list"),

     path(
        "specialities/",
        views.specialities,
        name="specialities"
    ),

    path(
        "specialities/add/",
        views.add_speciality,
        name="add_speciality"
    ),

    path(
        "specialities/<int:speciality_id>/edit/",
        views.edit_speciality,
        name="edit_speciality"
    ),

    path(
        "specialities/<int:speciality_id>/delete/",
        views.delete_speciality,
        name="delete_speciality"
    ),

    # =====================================================
    # TRANSACTIONS
    # =====================================================

    path(
        "transactions/",
        views.transaction_list,
        name="transaction_list"
    ),
]



