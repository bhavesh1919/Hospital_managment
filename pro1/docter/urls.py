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
    
    
    path('account/', views.account, name='account'),
    path('appointment/', views.Appointment, name='appointment'),
    path('available_timming/', views.avilable_timming, name='avilable_timming'),
    path('chat/', views.chat, name='chat'),
    path('docter_blog/', views.docter_blog, name='docter_blog'),
    path('docter_change_password/', views.docter_change_password, name='docter_change_password'),
    path('docter_dash/', views.docter_Dash, name='docter_dash'),
    path('docter_payment/', views.docter_payment, name='docter_payment'),
    path('docter_profile_settings/', views.docter_profile_settings, name='docter_profile_settings'),
    path('docter_specialties/', views.docter_specialties, name='docter_specialties'),
    path('invoice/', views.invoice, name='invoice'),
    path('my_patients/', views.my_patients, name='my_patients'),
    path('request/', views.request_page, name='request'),
    path('review/', views.review, name='review'),
]
