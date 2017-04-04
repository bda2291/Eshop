from django.shortcuts import render
from .forms import SubscriberForm

def landing(request):
    name = "Denis"
    form = SubscriberForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        form.save()
    return render(request, 'landing/landing.html', locals())
