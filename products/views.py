from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import auth
from django.http import JsonResponse
import json
import decimal
from cart.forms import CartAddProductForm
from .utils import get_variant_picker_data
from django.template.response import TemplateResponse
from .models import *
from .forms import FacetedProductSearchForm
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet

def serialize_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    return json.JSONEncoder.default(obj)

def productlist(request, category_slug=None):
    username = auth.get_user(request).username
    category = None
    categories = ProductCategory.objects.filter(level__lte=0)
    # categories = ProductCategory.objects.filter(is_active=True)
    # for category in categories:
    #     print(type(category))
    #     print(type(category.get_children()[0]))
    products = Product.objects.filter(is_active=True)
    if category_slug:
        category = get_object_or_404(ProductCategory, slug=category_slug)
        products = products.filter(category__in=category.get_descendants(include_self=True))
    return render(request, 'products/list.html', locals())

def product(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_active=True)
    print(product.price, product.points)
    username = auth.get_user(request).username
    cart_product_form = CartAddProductForm()
    variant_picker_data = get_variant_picker_data(product)
    show_variant_picker = all([v.attributes for v in product.variants.all()])
    # session_key = request.session.session_key
    # if not session_key:
    #     request.session.cycle_key()

    return render(request, 'products/product.html', {'username': username, 'product': product, 'form': cart_product_form,
                                                     'show_variant_picker': show_variant_picker,
                                                     'variant_picker_data': variant_picker_data,
                                                     })

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('query', ''))[:5]
    s = []
    for result in sqs:
        print(result)
        d = {"value": result.name, "data": result.object.slug}
        s.append(d)
    output = {'suggestions': s}
    return JsonResponse(output)

class FacetedSearchView(BaseFacetedSearchView):
    form_class = FacetedProductSearchForm
    facet_fields = ['category', 'producer']
    template_name = 'search/search.html'
    paginate_by = 3
    context_object_name = 'object_list'