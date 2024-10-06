zfrom django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .forms import Registration, CustomAuthenticationForm
from django.contrib import messages as flash

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = Registration(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            #login(request, user)
            flash.success(request, 'Your account is successfully created')
            return redirect('/users/login')
    else:
        form = Registration()
    return render(request, 'users/signup.html', {'form': form, 'title': 'Sign Up'})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                flash.success(request, 'Logged in successfully')
                return redirect('/chat/')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form, 'title': 'Login'})
def log_out(request):
    print('loggin out....')
    logout(request)
    flash.success(request, 'Your are logged out')
    return redirect('/users/login')
