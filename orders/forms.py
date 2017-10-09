from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Order

class OrderCreateForm(forms.ModelForm):

    customer_name = forms.CharField(max_length=100, required=True, label='Customer_name',
                                    widget=forms.TextInput(attrs={'placeholder': 'Ф.И.О.'}))
    customer_phone = PhoneNumberField(required=True, label='Customer_phone',
                                      widget=forms.TextInput(attrs={'placeholder': 'номер телефона'}))
    customer_email = forms.EmailField(required=True, label='Customer_email',
                                      widget=forms.TextInput(attrs={'placeholder': 'e-mail'}))
    city = forms.CharField(max_length=100, label='City', widget=forms.TextInput(attrs={'placeholder': 'город'}))

    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 'city']

