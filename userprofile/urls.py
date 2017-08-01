from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^profile/', views.user_profile, name='user_profile'),
    url(r'^update_profile/', views.update_profile, name='update_profile'),
    url(r'^pick_up_points/', views.pick_up_points, name='pick_up_points')
]
