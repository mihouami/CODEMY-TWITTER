from django.shortcuts import render, get_object_or_404, redirect
from .models import Meep
from .forms import MeepForm
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from project.decorators import login_required_with_message
from users.models import Profile


def home(request):
    if request.user.is_authenticated:
        followed_profiles = request.user.profile.follows.all()
        meeps = Meep.objects.all().order_by("-date_added").filter(author__in=followed_profiles)
        form = MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.author = request.user.profile
                meep.save()
                return render(
                    request, "partials/meep.html", {"meep": meep, "form": MeepForm()}
                )
        context = {"meeps": meeps, "form": form}
        return render(request, "home.html", context)
    else:
        meeps = Meep.objects.all().order_by("-date_added")
        return render(request, "home.html", {"meeps": meeps})    


def check_meep(request):
    form = MeepForm(request.GET)
    context = {
        "field": as_crispy_field(form["meep"]),
        "valid": not form["meep"].errors,
    }
    return render(request, "partials/meepfield.html", context)

@login_required_with_message
def Like_unlike(request, pk):
    meep = get_object_or_404(Meep, pk=pk)
    if request.user in meep.likes.all():
        meep.likes.remove(request.user)
    else:
        meep.likes.add(request.user)
    return render(request, 'partials/likes.html', {'meep':meep})


@login_required_with_message
def Like_unlike2(request, pk, pk2):
    meep = get_object_or_404(Meep, pk=pk)
    profile = get_object_or_404(Profile, pk=pk2)
    meeps = profile.meeps.all()
    liked_meeps = Meep.objects.filter(likes=profile.user)
    
    if request.user in meep.likes.all():
        meep.likes.remove(request.user)
    else:
        meep.likes.add(request.user)
    context = {"profile": profile, "meeps": meeps, "liked_meeps":liked_meeps}
    # return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'partials/col.html', context)

    

