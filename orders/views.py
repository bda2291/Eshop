from django.shortcuts import render
from django.http import JsonResponse
from .models import ProductsInBasket

def basket_adding(request):
    return_dict = {}
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")

    new_product, created = ProductsInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, defaults={'number':nmb})
    if not created:
        new_product.number += int(nmb)
        new_product.save(force_update=True)

    products_in_basket = ProductsInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb
    return_dict["products"] = []

    for item in products_in_basket:
        product_dict = {}
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_itom
        product_dict["nmb"] = item.number
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)

def basket_remove(request):
    return_dict = {}
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get("product_id")
