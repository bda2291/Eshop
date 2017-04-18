from django.shortcuts import render
from django.contrib import auth
from products.models import *


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    username = auth.get_user(request).username

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    return render(request, 'products/product.html', locals())

