from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default_profile_picture.png', blank=True, null=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    bio = models.CharField(max_length=150, blank=True, null=True)

class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    created = models.DateTimeField(auto_now_add=True)
