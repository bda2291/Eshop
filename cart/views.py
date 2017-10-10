from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from products.models import Product, Offer
from .cart import Cart
from .forms import CartAddProductForm
# from discount.forms import DiscountApllyForm

@csrf_exempt
@require_POST
@login_required(login_url='auth:login')
def CartAdd(request):
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if int(cd['quantity']) < 1 or int(cd['quantity']) > 1000:
            return redirect(request.META.get('HTTP_REFERER'))
        offer = get_object_or_404(Offer, slug=cd['product_slug'])
        cart.add(offer=offer, price_per_itom=cd['price_per_itom'], quantity=cd['quantity'],
                 update_quantity=cd['update'])
        request.session.pop('points', None)
    return redirect('cart:CartDetail')

@csrf_exempt
@login_required(login_url='auth:login')
def CartRemove(request, offer_slug):
    cart = Cart(request)
    # offer = get_object_or_404(Offer, slug=offer_slug)
    cart.remove(offer_slug)
    request.session.pop('points', None)
    return redirect('cart:CartDetail')

@csrf_exempt
@login_required(login_url='auth:login')
def CartDetail(request):
    user = auth.get_user(request)
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'product_slug': item['offer'].slug,
                                            'price_per_itom': item['price'],
                                            'update': True
                                        })
    # discount_apply_form = DiscountApllyForm()
    return render(request, 'cart/detail.html', {'username': user.username})
                                                # 'discount_apply_form': discount_apply_form})
