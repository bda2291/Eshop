from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^landing/', views.landing, name='landing'),
    url(r'^$', views.home, name='home'),
]