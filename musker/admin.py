from django.contrib import admin
from .models import Meep

@admin.register(Meep)
class MeepAdmin(admin.ModelAdmin):
    list_display = ["meep", "author", "date_added", "date_modified"]