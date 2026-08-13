from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Register(models.Model):
    name=models.CharField(max_length=25)
    phone=models.IntegerField()
    email=models.EmailField()
    password=models.CharField()


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    ROLE_CHOICES=[
        ("Pateint","Pateint"),
        ("Docter","Docter"),
    ]
    role = models.CharField(max_length=10,choices=ROLE_CHOICES)


    def __str__(self):
     return f"{self.user.username}({self.role})"

class Patient(models.Model):
    profile= models.OneToOneField(Profile,on_delete=models.CASCADE)
    type=models.TextField(blank=True,null=True)
    profile_photo = models.ImageField(upload_to="profile/")
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    dob = models.DateField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    blood = models.CharField(max_length=5)
    address = models.TextField(default='')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
      return f"Patient:{self.profile.user.username}"

class Docter(models.Model):
    profile= models.OneToOneField(Profile,on_delete=models.CASCADE)
    specalist = models.CharField(max_length=255)

    def __str__(self):
       return f"Docter:{self.profile.user.username}"



