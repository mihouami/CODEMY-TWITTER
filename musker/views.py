from django.shortcuts import render, get_object_or_404, redirect
from .models import Meep
from .forms import MeepForm
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from project.decorators import login_required_with_message
from users.models import Profile
from django.core.mail import send_mail
from django.contrib import messages


def home(request):
    if request.user.is_authenticated:
        followed_profiles = request.user.profile.follows.all()
        q = request.GET.get('q')
        if q:
            meeps = (
                Meep.objects.all()
                .order_by("-date_added")
                .filter(author__in=followed_profiles, meep__contains=q)
            )
        else:
            meeps = (
                Meep.objects.all()
                .order_by("-date_added")
                .filter(author__in=followed_profiles)
            )
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
    return render(request, "meep_detail.html", {"meep": meep})


def like_unlike3(request, pk):
    meep = get_object_or_404(Meep, pk=pk)
    child = meep.child_meep
    if request.user in child.likes.all():
        child.likes.remove(request.user)
    else:
        child.likes.add(request.user)
    return render(request, "meep_detail.html", {"meep": meep})


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
    context = {"profile": profile, "meeps": meeps, "liked_meeps": liked_meeps}
    # return redirect(request.META.get('HTTP_REFERER'))
    return render(request, "partials/col.html", context)


def meep_share(request, pk):
    meep = get_object_or_404(Meep, pk=pk)
    return render(request, "meep_share.html", {"meep": meep})


def send_meep_link(request, pk):
    email = request.POST.get("email")
    subject = request.POST.get("object")
    message = request.POST.get("body")
    final_message = f"""
            Hello,\n
            Check out this meep : http://127.0.0.1:8000/meep_share/{pk}/\n
            Message from the sender : {message}
            """
    send_mail(
        subject,  # Subject of the email
        final_message,  # Message of the email
        "from@example.com",  # Sender's email address
        [email],  # List of recipients' email addresses
        fail_silently=False,  # Set to True to suppress errors
    )
    return redirect(request.META.get("HTTP_REFERER"))


def share_meep_profile(request, pk):
    if request.user.is_authenticated:
        child_meep = get_object_or_404(Meep, pk=pk)
        meep = Meep(author=request.user.profile, meep="None", child_meep=child_meep)
        meep.save()
        return redirect("home")
    


@login_required_with_message
def delete_meep(request, pk):
    meep = get_object_or_404(Meep, pk=pk)
    if request.user.id == meep.author.user.id:
        meep.delete()
        messages.success(request, 'Meep deleted with success')
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.warning(request, 'Your are not allowed to delete this meep')
        return redirect(request.META.get("HTTP_REFERER"))
    
@login_required_with_message
def update_meep(request, pk):
    meep = get_object_or_404(Meep, pk=pk)
    form = MeepForm(request.POST or None, instance=meep)
    if request.user.id == meep.author.user.id:
        if request.method == 'POST':
            form.save()
            return render(request, 'meep_detail.html', {'meep':meep})
        return render(request, 'partials/meep_form.html', {'form':form, 'meep':meep})
    else:
        messages.warning(request, 'Your are not allowed to update this meep')
        return redirect('profile', pk=request.user.id)

