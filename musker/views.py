from django.shortcuts import render, redirect
from .models import Meep
from .forms import MeepForm

def home(request):
    meeps = Meep.objects.all().order_by('-date_added')
    form = MeepForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            meep = form.save(commit=False)
            meep.author = request.user.profile
            meep.save()
            return redirect('home')
    context = {'meeps':meeps, 'form':form}
    return render(request, 'home.html', context)
