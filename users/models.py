# users/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Profile Model
class Profile(models.Model):
    # One-to-One relationship with the built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # User Profile Fields
    bio = models.TextField(max_length=500, blank=True, null=True)
    # Note: You'll need to set up media handling later for the profile_picture field
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # To meet the requirements for followers/following counts (we'll implement the actual follow logic later)
    # We will add reverse relationships for followers/following in the next phase
    
    def __str__(self):
        return f"{self.user.username} Profile"

# Signal to create a Profile automatically when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save the Profile automatically when the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Follow(models.Model):
    # The user who is doing the following
    follower = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following' # Access users this user follows (user.following.all())
    )
    # The user who is being followed
    followed = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='followers' # Access users who follow this user (user.followers.all())
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can only follow another user once
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"