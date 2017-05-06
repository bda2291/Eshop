from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Discount
from .forms import DiscountApllyForm


@require_POST
def DiscountApply(request):
    now = timezone.now()
    form = DiscountApllyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            discount = Discount.objects.get(code__iexact=code,
                                      valid_from__lte=now,
                                      valid_to__gte=now,
                                      active=True)
            request.session['discount_id'] = discount.id
        except Discount.DoesNotExist:
            request.session['discount_id'] = None
            
    return redirect('cart:CartDetail')


