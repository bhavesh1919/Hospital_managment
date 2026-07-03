from django.db import models


# Create your models here.
class Register(models.Model):
    name=models.CharField(max_length=25)
    phone=models.IntegerField()
    email=models.EmailField()
    password=models.CharField()
