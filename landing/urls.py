from django.conf.urls import url
from landing import views

urlpatterns = [
    url(r'^landing/', views.landing, name='landing'),
]