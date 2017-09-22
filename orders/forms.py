from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Order

class OrderCreateForm(forms.ModelForm):

    customer_name = forms.CharField(max_length=64, required=True, help_text='Введите Ваше полное Ф.И.О')
    customer_phone = PhoneNumberField(required=True, help_text='Введите Ваш номер телефона')
    customer_email = forms.EmailField(required=True, help_text='Введите Ваш e-mail')
    city = forms.CharField(max_length=100, help_text='Введите Ваш город')

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 'city']

