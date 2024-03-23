from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def profiles_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        context = {'profiles':profiles}
        return render(request, 'profiles_list.html', context)
    else:
        messages.warning(request, 'You must be logged In to access this page!')
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, pk=pk)
        meeps = profile.meeps.all()
        context = {'profile':profile, 'meeps':meeps}
        return render(request, 'profile.html', context)
    else:
        messages.warning(request, 'You must be logged In to access this page!')
        return redirect('home')

@login_required(login_url="/")
def follow_unfollow(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if profile in request.user.profile.follows.all():
        request.user.profile.follows.remove(profile)
    else:
        request.user.profile.follows.add(profile)
    return redirect('profile', pk=pk)




