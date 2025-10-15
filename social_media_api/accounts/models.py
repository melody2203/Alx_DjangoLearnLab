from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    def is_following(self, user):
        """Check if current user is following the given user"""
        return self.following.filter(id=user.id).exists()
    
    def follow(self, user):
        """Follow a user"""
        if not self.is_following(user) and self != user:
            self.following.add(user)
            return True
        return False
    
    def unfollow(self, user):
        """Unfollow a user"""
        if self.is_following(user):
            self.following.remove(user)
            return True
        return False
    
    def get_followers(self):
        """Get all followers"""
        return self.followers.all()
    
    def get_following(self):
        """Get all users being followed"""
        return self.following.all()