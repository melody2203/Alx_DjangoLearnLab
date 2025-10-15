from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields you need
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Following relationships
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow another user"""
        if user != self and not self.following.filter(id=user.id).exists():
            self.following.add(user)
            return True
        return False
    
    def unfollow(self, user):
        """Unfollow a user"""
        if self.following.filter(id=user.id).exists():
            self.following.remove(user)
            return True
        return False
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()