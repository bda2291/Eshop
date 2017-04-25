from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts/profile')

    else:
        user = auth.get_user(request)
        profile = user.profile
        form = UserProfileForm(instance=profile)

    args = {}
    args['form'] = form
    args['username'] = user.username
    return render_to_response('userprofile/profile.html', args)



