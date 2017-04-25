from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    print(request.POST)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:CartDetail')

def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')

def CartDetail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', locals())
