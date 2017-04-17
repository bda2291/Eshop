from django.shortcuts import render
from .forms import SubscriberForm
from django.contrib import auth
from products.models import *

def landing(request):
    form = SubscriberForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(form.cleaned_data)
        form.save()

    return render(request, 'landing/landing.html', locals())


def home(request):
    product_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    product_images_phones = product_images.filter(product__category__id=1)
    product_images_watches = product_images.filter(product__category__id=2)
    username = auth.get_user(request).username
    return render(request, 'landing/home.html', locals())
