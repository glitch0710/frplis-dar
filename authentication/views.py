from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

def index(request):
    if request.method == 'GET':
        return render(request, 'authentication/login.html')
    else:
        try:
            user = authenticate(request, username=request.POST.get('username', ''), password=request.POST.get('password', ''))
            if user is None:
                messages.error(request, 'Wrong username or password. Please try again.')
                return redirect('authentication:index')
            else:
                login(request, user)
                if request.user.is_staff and request.user.is_superuser:
                    return redirect('dashboard:user_dashboard')
                else:
                    if user.groups.all()[0].id == 1:
                        # return redirect('user_home')
                        return HttpResponse('technical')
                    elif user.groups.all()[0].id == 2:
                        # return redirect('user_engineer')
                        return HttpResponse('engineer')
        except ValueError:
            messages.error(request, 'Wrong username or password. Please try again.')
            return redirect('authentication:index')

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('authentication:index')

def forgot_password(request):
    return render(request, 'authentication/forgot-password.html')
