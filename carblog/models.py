from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Blog(models.Model):
    title = models.CharField(max_length=60)
    car = models.ForeignKey("Car", on_delete=models.CASCADE, related_name="subject")
    timestamp = models.DateTimeField(auto_now_add=True)

class Car(models.Model):
    price = models.IntegerField()
    brand = models.CharField(max_length=30)
    year = models.IntegerField()
    theModel = models.CharField(max_length=50)