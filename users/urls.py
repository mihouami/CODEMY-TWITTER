from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .forms import (
    CustomPasswordResetEmailForm,
    CustomPasswordResetForm,
)
from django.urls import reverse_lazy

urlpatterns = [
    path("profiles/", profiles_list, name="profiles_list"),
    path("profile/<int:pk>/", profile, name="profile"),
    path("follow_unfollow/<int:pk>/", follow_unfollow, name="follow_unfollow"),
    path("update_profile/<int:pk>/", update_profile, name="update_profile"),
    path("delete_image/<int:pk>/", delete_image, name="delete_image"),
    
    # Login URLs
    path("login2/", login_user2, name="login2"),
    # path("login/", login_user, name="login"),
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    
    # Logout URLs
    path("logout/", logout_user, name="logout"),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Register URL
    path("register/", register_user, name="register"),
    
    # Password Reset URLs
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetEmailForm,
            template_name="custom_password_reset.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="custom_password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            form_class = CustomPasswordResetForm,
            template_name = "custom_password_reset_confirm.html",
            success_url = reverse_lazy("login2")),
        name="password_reset_confirm",
    ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='custom_password_reset_complete.html'), name='password_reset_complete'),
    
    # Password Change URLs
    path(
        "password_change/",
        CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    # path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="custom_password_change_done.html",), name='password_change_done'),
]
