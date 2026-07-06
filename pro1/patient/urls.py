"""
URL configuration for pro1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [
    
   path('patient',views.patient_dashboard),
   
    path('patients_appointment/', views.patients_appointment, name='patients_appointment'),

    path('patient_account/', views.patient_account, name='patient_account'),

    path('patient_invoice/', views.patient_invoice, name='patient_invoice'),

    path('medical_record/', views.medical_record, name='medical_record'),

    path('medical_details/', views.medical_details, name='medical_details'),

    path('favourites/', views.favourites, name='favourites'),

    path('dependent/', views.dependent, name='dependent'),
]
