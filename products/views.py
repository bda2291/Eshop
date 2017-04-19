from django.shortcuts import render, render_to_response
from django.contrib import auth
from products.models import *


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    username = auth.get_user(request).username

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    return render(request, 'products/product.html', locals())

def search(request):
    search_text = request.POST.get('search_text')

    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__name__contains=search_text)

    return render_to_response('products/search.html', {'products_images': products_images})