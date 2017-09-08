from django import forms

#PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    #quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    quantity = forms.CharField(required=True, widget=forms.TextInput(attrs={
                                                        'id': 'quantity',
                                                        'name': 'quantity',
                                                        'type': 'number',
                                                        'value': '0',
                                                        'onchange': 'calculate()'}))
    product_slug = forms.CharField(label="product_slug", widget=forms.TextInput(attrs={
                                                        'id': 'product_slug',
                                                        'name': 'product_slug',
                                                       'type': 'hidden'}))
    price_per_itom = forms.IntegerField(label="price_per_itom", widget=forms.TextInput(attrs={
                                                        'id': 'price_per_itom',
                                                        'name': 'price_per_itom',
                                                        'type': 'hidden'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

