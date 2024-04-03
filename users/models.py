from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from PIL import Image


# Custom User
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    mobile = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="images/", default="images/default.jpg")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


    def save(self, *args, **kwargs):
        # Call the original save method to ensure other functionalities are preserved
        super().save(*args, **kwargs)
        # Open the image file
        img = Image.open(self.image.path)
        # Resize the image, Here, (300, 300) is the desired size (width, height)
        img.thumbnail((300, 300))
        # Save the modified image back to the same path
        img.save(self.image.path)
        # Call the original save method again to ensure all modifications are saved
        super().save(*args, **kwargs)


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
