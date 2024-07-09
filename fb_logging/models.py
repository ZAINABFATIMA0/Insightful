from django.conf import settings
from django.db import models
from social_django.models import UserSocialAuth

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
