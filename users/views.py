from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from project.decorators import (
    redirect_if_logged_in,
    redirect_if_logged_out,
    login_required_with_message,
)
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegisterForm, UserUpdateForm


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
    meeps = profile.meeps.all()
    context = {"profile": profile, "meeps": meeps}
    return render(request, "profile.html", context)


# FOLLOW - UNFOLLOW VIEW
@login_required_with_message
def follow_unfollow(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if profile in request.user.profile.follows.all():
        request.user.profile.follows.remove(profile)
    else:
        request.user.profile.follows.add(profile)
    return redirect("profile", pk=pk)


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
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "You have been successfully Registered")
            return redirect('login2')
    return render(request, 'register.html', {'form':form})


# UPDATE PROFILE
@login_required_with_message
def update_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.user.id != user.id:
        messages.warning(request, 'You are not allowed to access this page.')
        return redirect('profile', pk=user.id)
    elif request.user.id == user.id:
        form = UserUpdateForm(request.POST or None, instance=user)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Updated!')
                return redirect('update_profile', pk=user.id)
        return render(request, 'update_profile.html', {'form':form})
