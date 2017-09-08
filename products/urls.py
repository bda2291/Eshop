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
from .views import FacetedSearchView, autocomplete, productslist, product, categorieslist, producerslist


urlpatterns = [
    #url(r'^product/(?P<product_id>\w+)/$', views.product, name='product'),
    url(r'^$', producerslist, name='ProductList'),
    url(r'^autocomplete/$', autocomplete),
    url(r'^find/$', FacetedSearchView.as_view(), name='haystack_search'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', product, name='Product'),
    url(r'^(?P<producer_slug>[-\w]+)/$', categorieslist, name='CategoriesListByProducer'),
    url(r'^(?P<producer_slug>[-\w]+)/(?P<category_slug>[-\w]+)/$', productslist, name='ProductListByCategory')
]
