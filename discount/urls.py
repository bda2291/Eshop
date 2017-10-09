from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^apply', views.DiscountApply, name='apply'),
    url(r'^create', views.CreateDiscount, name='create'),
    url(r'^points', views.PointsApply, name='points'),
    url(r'^revoke_points', views.PointsRevoke, name='revoke_points')
]