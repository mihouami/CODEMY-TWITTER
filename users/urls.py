from django.urls import path
from .views import *

urlpatterns = [
    path("profiles/", profiles_list, name="profiles_list"),
    path("profile/<int:pk>/", profile, name="profile"),
    path("follow_unfollow/<int:pk>/", follow_unfollow, name="follow_unfollow"),
    path("login/", login_user, name="login"),
    path("login2/", login_user2, name="login2"),
    path("logout/", logout_user, name="logout"),
]
