from django.db import models
from users.models import Profile
from django.core.validators import MinLengthValidator, MaxLengthValidator
from users.models import CustomUser


class Meep(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="meeps")
    meep = models.CharField(
        max_length=300,
        unique=False,
        blank=False,
        null=False,
        validators=[MinLengthValidator(5), MaxLengthValidator(255)],
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name="liked_by", blank=True)

    def __str__(self):
        return self.meep
