from django.db import models
from users.models import Profile

class Meep(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="meeps")
    meep = models.CharField(max_length=255, blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meep
