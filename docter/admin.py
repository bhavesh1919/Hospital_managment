from django.contrib import admin
from .models import Availability

# Register your models here.

admin.site.register(Availability)

from django.contrib import admin
from .models import (
    Speciality,
    DoctorSpeciality,
    DoctorService
)

from django.contrib import admin
from .models import Speciality, DoctorSpeciality, DoctorService


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(DoctorSpeciality)
class DoctorSpecialityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor",
        "speciality",
        "created_at",
    )

    list_filter = ("speciality",)


@admin.register(DoctorService)
class DoctorServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "doctor_speciality",
        "service_name",
        "price",
        "created_at",
    )

    search_fields = ("service_name",)