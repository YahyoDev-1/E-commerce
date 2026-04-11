from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class GENDER(models.TextChoices):
        ERKAK = 'Erkak', 'Erkak'
        AYOL = 'Ayol', 'Ayol'
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    gender = models.CharField(choices=GENDER.choices, max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    confirmation_code = models.CharField(max_length=100)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Seller(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.first_name