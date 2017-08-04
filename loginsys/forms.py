from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    parent = forms.CharField(required = False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'parent')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if self.cleaned_data.get('parent'):
            user.parent = User.objects.get(username=self.cleaned_data['parent'])
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user