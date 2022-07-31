from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="poster")
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=255)

    def serialize(self):
        return{
            "userName": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
class Following(models.Model):
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="userFollowing")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="userFollowers")
   

class Like(models.Model):
    likedPost = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="l_post")
    liker = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_like")
