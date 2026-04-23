from django.db import models
from django.contrib.auth.models import AbstractUser
from cities_light.models import Country


# Create your models here.

class User(AbstractUser):
    gender = models.CharField(max_length=20, choices=(('erkak', 'erkak'), ('ayol', 'ayol')))
    phone = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="users/", null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=50)
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username
