from django.db import models

from app1.models import Docter,Patient
from django.contrib.auth.models import User




class Availability(models.Model):

    STATUS = (
        ("Available", "Available"),
        ("Unavailable", "Unavailable"),
    )

    DAYS = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    day = models.CharField(
        max_length=20,
        choices=DAYS
    )

    start_time = models.TimeField()
    

    end_time = models.TimeField()

    duration = models.IntegerField()

    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.doctor.username} - {self.day}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Docter, on_delete=models.CASCADE)
    record_name = models.CharField(max_length=200)
    record_date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    comments = models.TextField(blank=True)
    report = models.FileField(upload_to="medical_records/", blank=True)