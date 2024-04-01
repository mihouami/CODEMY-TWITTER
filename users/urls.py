from django.urls import path
from .views import *

urlpatterns = [
    path("profiles/", profiles_list, name="profiles_list"),
    path("profile/<int:pk>/", profile, name="profile"),
    path("follow_unfollow/<int:pk>/", follow_unfollow, name="follow_unfollow"),
    path("update_profile/<int:pk>/", update_profile, name="update_profile"),
    path("delete_image/<int:pk>/", delete_image, name="delete_image"),

    # Login URLs
    path("login/", login_user, name="login"),
    path("login2/", login_user2, name="login2"),

    # Logout URLs
    path("logout/", logout_user, name="logout"),

    # Register URL
    path("register/", register_user, name="register"),
]
