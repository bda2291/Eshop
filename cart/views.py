from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from products.models import Product, Offer
from .cart import Cart
from .forms import CartAddProductForm
# from discount.forms import DiscountApllyForm

@csrf_exempt
@require_POST
def CartAdd(request):
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        offer = get_object_or_404(Offer, slug=cd['product_slug'])
        cart.add(offer=offer, price_per_itom=cd['price_per_itom'], quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:CartDetail')

def CartRemove(request, offer_slug):
    cart = Cart(request)
    # offer = get_object_or_404(Offer, slug=offer_slug)
    cart.remove(offer_slug)
    return redirect('cart:CartDetail')

def CartDetail(request):
    user = auth.get_user(request)
    cart = Cart(request)
    for item in cart:
        print(item)
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'product_slug': item['offer'].slug,
                                            'price_per_itom': item['price'],
                                            'update': True
                                        })
    # discount_apply_form = DiscountApllyForm()
    return render(request, 'cart/detail.html', {'username': user.username,'cart': cart})
                                                # 'discount_apply_form': discount_apply_form})
