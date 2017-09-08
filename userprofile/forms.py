from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, PickUpRequest

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('city', 'phone')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class PickUpPointsForm(forms.ModelForm):
    class Meta:
        model = PickUpRequest
        fields = ('requisites',)
