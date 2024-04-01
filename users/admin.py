from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# Unregister Group
admin.site.unregister(Group)

# Register Profile
admin.site.register(Profile)


# Mix Profile Info into CustomUser Info
class ProfileInline(admin.StackedInline):
    model = Profile


# Register Custom User
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = [
        "username",
        "email",
        "mobile",
        "is_superuser",
        "date_joined",
        "last_login",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email", "mobile", "image")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "mobile", "password1", "password2"),
            },
        ),
    )

    list_filter = [
        "username",
        "is_staff",
        "is_superuser",
        "is_active",
        "email",
        "mobile",
    ]
    search_fields = ["username", "email", "mobile"]
    ordering = ["date_joined", "last_login"]
    # date_hierarchy
    # raw_id_fields
    # prepopulated_fields
    # model = CustomUser
    # fields = ['username']
