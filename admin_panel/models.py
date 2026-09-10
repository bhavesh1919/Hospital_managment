from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class WebsiteSetting(models.Model):
    website_name = models.CharField(max_length=200, default="DOCCURE")
    website_logo = models.ImageField(
        upload_to="website/",
        null=True,
        blank=True
    )
    favicon = models.ImageField(
        upload_to="website/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.website_name





class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(
        upload_to="admin_profile/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username