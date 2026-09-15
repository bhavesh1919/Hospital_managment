
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
    path("logout/", views.Logout, name="logout"),
    path('delete-doctor/<int:id>/', views.delete_doctor, name='delete_doctor'),
    path('delete-patient/<int:id>/', views.delete_patient, name='delete_patient'),
    path('specialities/', views.specialities, name='specialities'),
    path('specialities/add/', views.add_speciality, name='add_speciality'),
    path('specialities/<int:speciality_id>/edit/', views.edit_speciality, name='edit_speciality'),
    path('specialities/<int:speciality_id>/delete/', views.delete_speciality, name='delete_speciality'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('approve-appointment/<int:id>/', views.approve_appointment, name='admin_approve_appointment'),
    path('reject-appointment/<int:id>/', views.reject_appointment, name='admin_reject_appointment'),


   path(
        'categories/',
        views.categories,
        name='categories'
    ),

    path(
        'products/',
        views.products,
        name='products'
    ),

    path(
        'purchase/',
        views.purchase,
        name='purchase'
    ),

    path(
        'sales/',
        views.sales,
        name='sales'
    ),

    path(
        'transactions/',
        views.transactions_list,
        name='transactions_list'
    ),


    path('outstock/', views.outstock, name='outstock'),


# =========================
# ADD
# =========================

path(
    'products/add/',
    views.add_product,
    name='add_product'
),

path(
    'purchase/add/',
    views.add_purchase,
    name='add_purchase'
),

path(
    'supplier/add/',
    views.add_supplier,
    name='add_supplier'
),

# =========================
# EDIT
# =========================

path(
    'products/edit/<int:id>/',
    views.edit_product,
    name='edit_product'
),

path(
    'purchase/edit/<int:id>/',
    views.edit_purchase,
    name='edit_purchase'
),

# =========================
# EXPIRED
# =========================

path(
    'expired/',
    views.expired,
    name='expired'
),







]



