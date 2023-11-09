from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(null=True, blank=True, max_length=20)

class Profile(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField()
    location = models.CharField(max_length=100)



