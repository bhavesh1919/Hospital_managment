from django.db import models
import django.utils.timezone

# Create your models here.
from app1.models import Patient,Docter
from docter.models import Availability
class appointment(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
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

    appointment_day = models.CharField(
        max_length=20
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

   

    def __str__(self):
        return f"{self.patient.fname} - Dr. {self.docter.display_name}"