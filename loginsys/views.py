from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from .forms import RegistrationForm

@csrf_exempt
def login(request):
    args = {}
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "User is not found"
            return render_to_response('login/login.html', args)

    else:
        return render_to_response('login/login.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/')

@csrf_exempt
def register(request):
    args= {}
    args['form'] = RegistrationForm()
    if request.POST:
        newuser_form = RegistrationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password1'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('login/register.html', args)



