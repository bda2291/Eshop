from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import auth
from cart.forms import CartAddProductForm
from .models import *

def productlist(request, category_slug=None):
    category = None
    categories = ProductCategory.objects.filter(level__lte=0)
    products = Product.objects.filter(is_active=True)
    if category_slug:
        category = get_object_or_404(ProductCategory, slug=category_slug)
        products = products.filter(category__in=category.get_descendants(include_self=True))
    return render(request, 'products/list.html', locals())

def product(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_active=True)
    username = auth.get_user(request).username
    cart_product_form = CartAddProductForm()
    # session_key = request.session.session_key
    # if not session_key:
    #     request.session.cycle_key()

    return render(request, 'products/product.html', locals())

def search(request):
    search_text = request.POST.get('search_text', '')
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__name__contains=search_text)
    # products_images = SearchQuerySet().auto_query(search_text)
    # q_spell = products_images.spelling_suggestion()
    # results = SearchQuerySet().filter(content=search_text)

    return render_to_response('products/search.html', {'products_images': products_images})