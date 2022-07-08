from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    imageURL = models.CharField(max_length=150)
    category = models.CharField(max_length=20)
    isActive = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item")
    price = models.IntegerField()

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched")

class Comment(models.Model):
    message = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="thePost")
