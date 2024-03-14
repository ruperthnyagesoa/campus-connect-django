from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class Post(models.Model):
    text = models.TextField(default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} posted: {self.text}"
    
    def is_content_valid(self):
        return len(self.text) > 10
    # def formatted_date(self):
    #     self.created_at = datetime(self.created_at)
    #     return self.created_at.strftime("%b %d, %Y, %I:%M %p")

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
    def number_of_followers(self):
        return self.following.username.count()
    

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_by')
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.post}"
    

