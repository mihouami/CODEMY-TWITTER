from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


# Custom User
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    mobile = models.CharField(max_length=10, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


# Profile
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )

    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


# Make Profile when new User is added
def make_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Make the new profile follow himself
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(make_profile, sender=CustomUser)
