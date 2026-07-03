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
from app1 import views


urlpatterns = [
    
    path('',views.index),
    path('login/',views.Login),
    path('register/',views.Registr),
   path('docter_Registr/',views.docter_Registr), 
   path('docter_dash/',views.docter_Dash),
   path('about-us/',views.about_us),
   path('contact/',views.contact),
   path('admin_dash/',views.admin_dash),
   path('patient',views.patient_dashboard),
]
