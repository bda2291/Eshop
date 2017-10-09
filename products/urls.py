"""Eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
import mptt_urls
from .views import productslist, product, categorieslist, producerslist
from .models import ProductCategory


urlpatterns = [
    #url(r'^product/(?P<product_id>\w+)/$', views.product, name='product'),
    url(r'^$', producerslist, name='ProductList'),

    # Uncomment for elasticsearch

    # url(r'^autocomplete/$', autocomplete),
    # url(r'^find/$', FacetedSearchView.as_view(), name='haystack_search'),


    url(r'^product/(?P<product_slug>[-\w]+)/$', product, name='Product'),
    url(r'^(?P<producer_slug>[-\w]+)/(?P<path>.*)',
        mptt_urls.view(model=ProductCategory, view=categorieslist, slug_field='slug'),
        name='CategoriesListByProducer'),
    # url(r'^(?P<producer_slug>[-\w]+)/$', categorieslist, name='CategoriesListByProducer'),
    url(r'^(?P<producer_slug>[-\w]+)/(?P<category_slug>[-\w]+)/$', productslist, name='ProductListByCategory')
]
