from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import auth
from django.http import JsonResponse
from cart.forms import CartAddProductForm
from .models import *
from .forms import FacetedProductSearchForm
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet

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