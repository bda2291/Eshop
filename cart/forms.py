from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.CharField(widget=forms.TextInput(attrs={
                                                        'id': 'quantity',
                                                        'name': 'quantity',
                                                        'type': 'number',
                                                        'min': '1',
                                                        'max': '1000',
                                                        'value': '1',
                                                        'onchange': 'calculate()'}))
    product_slug = forms.CharField(widget=forms.TextInput(attrs={
                                                        'id': 'product_slug',
                                                        'name': 'product_slug',
                                                        'type': 'hidden'}))
    price_per_itom = forms.IntegerField(widget=forms.TextInput(attrs={
                                                        'id': 'price_per_itom',
                                                        'name': 'price_per_itom',
                                                        'type': 'hidden'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

