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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^accounts/', include('userprofile.urls')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^order/', include('orders.urls', namespace='orders')),
    # url(r'^search/', include('haystack.urls')),
    url(r'^', include('products.urls', namespace='products')),
    url(r'^', include('landing.urls')),
    url(r'^', include('orders.urls')),
]\
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
