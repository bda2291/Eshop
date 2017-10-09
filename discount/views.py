import uuid
from datetime import datetime
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.contrib import auth
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Discount
from .forms import DiscountApllyForm

@login_required
@require_POST
@csrf_exempt
def PointsApply(request):
    request.session['points'] = True
    return redirect('cart:CartDetail')

@login_required
@require_POST
@csrf_exempt
def PointsRevoke(request):
    request.session.pop('points', None)
    return redirect('cart:CartDetail')

@require_POST
def DiscountApply(request):
    now = datetime.now()
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

@login_required
@require_POST
@csrf_exempt
def CreateDiscount(request):
    user = auth.get_user(request)
    Discount.objects.update_or_create(user=user, defaults={'code': str(uuid.uuid4()), 'valid_from': datetime.now(),
                                                           'valid_to': datetime.now()+timedelta(days=7), 'active': True})
    return redirect('profile:user_profile')




