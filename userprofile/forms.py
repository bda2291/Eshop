from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('description', 'city', 'website', 'phone')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')