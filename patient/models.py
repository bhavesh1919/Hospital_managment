from django.db import models

from app1.models import Patient, Docter
from docter.models import Availability


class appointment(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    docter = models.ForeignKey(
        Docter,
        on_delete=models.CASCADE
    )

    appointment = models.ForeignKey(
        Availability,
        on_delete=models.CASCADE
    )

    # Day of the appointment
    appointment_day = models.CharField(
        max_length=20
    )

    # Date selected for the appointment
    # Nullable because old records do not have this field
    appointment_date = models.DateField(
        null=True,
        blank=True
    )

    # Time selected for the appointment
    # Nullable because old records do not have this field
    appointment_time = models.TimeField(
        null=True,
        blank=True
    )

    # Automatically stores the date and time
    # when the appointment is created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    def __str__(self):
        return f"{self.patient.fname} - Dr. {self.docter.display_name}"


class Vital(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    blood_pressure = models.CharField(
        max_length=20
    )

    heart_rate = models.IntegerField()

    glucose_level = models.CharField(
        max_length=20
    )

    body_temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    bmi = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    spo2 = models.IntegerField()

    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    fbc_status = models.CharField(
        max_length=50,
        blank=True
    )

    # Automatically stores date and time
    # when the Vital record is created
    added_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient.username} - {self.added_on}"


class Favourite(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    docter = models.ForeignKey(
        Docter,
        on_delete=models.CASCADE
    )

    # Automatically stores date and time
    # when Favourite is created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient} - {self.docter.display_name}"