from django.db import models
from django.contrib.auth.models import AbstractUser

#Custom User
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    mobile = models.CharField(max_length=10, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

#Profile
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
                                    "self", 
                                    related_name="followed_by",
                                    symmetrical=False,
                                    blank=True)
    
    def __str__(self):
        return self.user.username


