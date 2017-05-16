from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^apply', views.DiscountApply, name='apply'),
    url(r'^create', views.CreateDiscount, name='create')
]