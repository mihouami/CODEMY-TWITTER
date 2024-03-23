from django.urls import path
from .views import *

urlpatterns = [
    path("profiles/", profiles_list, name="profiles_list"),
    path("profile/<int:pk>/", profile, name="profile"),
    path("follow_unfollow/<int:pk>/", follow_unfollow, name="follow_unfollow"),
]
