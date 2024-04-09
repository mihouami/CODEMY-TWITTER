from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from project.decorators import (
    redirect_if_logged_in,
    redirect_if_logged_out,
    login_required_with_message,
)
from .forms import LoginForm, UserRegisterForm, UserUpdateForm
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from musker.models import Meep, Profile


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "custom_password_change.html"

    def get_success_url(self):
        # Assuming request object is available in the view
        pk = self.request.user.pk
        return reverse_lazy("update_profile", kwargs={"pk": pk})

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Your password has been successfully changed.")
        return super().form_valid(form)


# PROFILE LIST VIEW
@login_required_with_message
def profiles_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    context = {"profiles": profiles}
    return render(request, "profiles_list.html", context)


# PROFILE DETAIL VIEW
@login_required_with_message
def profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    follows_count = profile.follows.count()
    followed_count = profile.followed_by.count()
    meeps = profile.meeps.all()
    liked_meeps = Meep.objects.filter(likes=profile.user)
    url = "/media/images/default.jpg"
    context = {
        "profile": profile,
        "meeps": meeps,
        "url": url,
        "liked_meeps": liked_meeps,
        "follows_count": follows_count,
        "followed_count": followed_count,
    }
    return render(request, "profile.html", context)


@login_required_with_message
def follows(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.user.id == profile.user.id:
        return render(request, 'follows.html', {'profile':profile})
    else:
        messages.warning(request, 'Your are not allowed to see other profiles followers list')
        return redirect('profile', pk=request.user.id)
    
@login_required_with_message
def followed(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.user.id == profile.user.id:
        return render(request, 'followed.html', {'profile':profile})
    else:
        messages.warning(request, 'Your are not allowed to see other profiles followers list')
        return redirect('profile', pk=request.user.id)


# FOLLOW - UNFOLLOW VIEW
@login_required_with_message
def follow_unfollow(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if profile in request.user.profile.follows.all():
        request.user.profile.follows.remove(profile)
    else:
        request.user.profile.follows.add(profile)
    return redirect(request.META.get("HTTP_REFERER"))


# LOGIN USERS 1
@redirect_if_logged_in
def login_user(request):
    if request.method == "POST":
        user = authenticate(
            email=request.POST.get("email"), password=request.POST.get("password")
        )
        if user is not None:
            login(request, user)
            messages.warning(request, "You have been successfully logged In")
            next = request.GET.get("next")
            if next:
                return redirect(next)
            return redirect("home")
        else:
            messages.warning(request, "Something went wrong")
            return redirect("login")
    return render(request, "login.html")


# LOGIN USERS 2
@redirect_if_logged_in
def login_user2(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password"),
            )
            if user is not None:
                login(request, user)
                messages.success(request, "You have been successfully logged In")
                next = request.GET.get("next")
                if next:
                    return redirect(next)
                return redirect("home")
            else:
                messages.warning(
                    request, "Invalid email or password. Please try again."
                )
    return render(request, "login2.html", {"form": form})


# LOGOUT USERS
@redirect_if_logged_out
def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged Out")
    return redirect("home")


# REGISTER USERS
@redirect_if_logged_in
def register_user(request):
    form = UserRegisterForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "You have been successfully Registered")
            return redirect("login2")
        else:
            messages.warning(request, "something went wrong")
    return render(request, "register.html", {"form": form})


# UPDATE PROFILE
@login_required_with_message
def update_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.user.id != user.id:
        messages.warning(request, "You are not allowed to access this page.")
        return redirect("profile", pk=user.id)
    elif request.user.id == user.id:
        form = UserUpdateForm(
            request.POST or None, request.FILES or None, instance=user
        )
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Profile Updated!")
                return redirect("profile", pk=user.id)
        return render(request, "update_profile.html", {"form": form})


# DELETE PROFILE PICTURE
@login_required_with_message
def delete_image(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.user.id == user.id:
        if user.image != "images/default.jpg":
            default_storage.delete(user.image.path)
            user.image = "images/default.jpg"
            user.save()
            return redirect("profile", pk=user.id)
        else:
            messages.warning(request, "Your are not allowed")
            return redirect("profile", pk=user.id)
    else:
        messages.success(request, "Not allowed")
        return redirect("profile", pk=user.id)
