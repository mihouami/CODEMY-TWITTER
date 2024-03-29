from django.shortcuts import render, redirect
from .models import Meep
from .forms import MeepForm
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field


def home(request):
    meeps = Meep.objects.all().order_by("-date_added")
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.author = request.user.profile
                meep.save()
                return redirect("home")
        context = {"meeps": meeps, "form": form}
        return render(request, "home.html", context)
    else:
        return render(request, "home.html", {"meeps": meeps})
    

def check_meep(request):
    form = MeepForm(request.GET)
    context={
        'field':as_crispy_field(form['meep']),
        'valid':not form['meep'].errors,
        }
    return render(request, 'partials/meepfield.html', context)

