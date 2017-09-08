from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.CartDetail, name='CartDetail'),
    url(r'^remove/(?P<offer_slug>[-\w]+)/$', views.CartRemove, name='CartRemove'),
    url(r'^add/$', views.CartAdd, name='CartAdd'),
]