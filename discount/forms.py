from django import forms

class DiscountApllyForm(forms.Form):
    code = forms.CharField()
