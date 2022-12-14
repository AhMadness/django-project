from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    
    # blank=True mean they are optional
    portfolio = models.URLField(blank=True)
    profpic = models.ImageField(upload_to='profile_pictures', blank=True) 
    
    def __str__(self):
        return self.user.username