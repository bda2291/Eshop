from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import auth
from decimal import Decimal
from .forms import UserProfileForm, PickUpPointsForm
from django.contrib.auth.decorators import login_required
from .models import PickUpRequest

@login_required
@csrf_exempt
def user_profile(request):
    user = auth.get_user(request)
    profile = user.profile
    discount = user.discount

    args = {}
    args['profile'] = profile
    args['discount'] = discount
    args['user_id'] = user.id
    args['username'] = user.username
    args['user'] = user
    return render_to_response('userprofile/profile.html', args)

@login_required
@csrf_exempt
def update_profile(request):
    user = auth.get_user(request)
    profile = user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile:user_profile')
    else:
        form = UserProfileForm(instance=profile)

        args = {}
        args['form'] = form
        args['user_id'] = user.id
        args['username'] = user.username
        return render_to_response('userprofile/update_profile.html', args)

@login_required
@csrf_exempt
def pick_up_points(request):
    user = auth.get_user(request)
    profile = user.profile
    if request.method == 'POST':
        form = PickUpPointsForm(request.POST)
        if form.is_valid():
            requisites = form.cleaned_data['requisites']
            PickUpRequest.objects.create(user=user, points=user.profile.user_points, requisites=requisites)
            profile.user_points = Decimal('0')
            profile.save()
            print(profile.user_points)
            return redirect('profile:user_profile')
    else:
        print(user.profile.user_points > 100)
        form = PickUpPointsForm()
        return render_to_response('userprofile/pick_up_points.html', {'user': user, 'form': form})


