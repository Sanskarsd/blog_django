from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    def __str__(self): return f'{self.user.username} profile'
