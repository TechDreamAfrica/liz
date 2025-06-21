from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from main.models import *
from django.contrib.auth.models import User, auth


def login(request):
    pagename = "User Login"


    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                messages.info(request, 'Admin Logged in Successfully')
                return redirect('admin-homepage')
            
            elif user.is_staff:
                auth.login(request, user)
                messages.info(request, 'Admin Logged in Successfully')
                return redirect('admin-homepage')
            
            else:
                messages.info(request, 'User Not an Admin: Can not Access This Page')
                return redirect('login')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    context = {
        'pagename':pagename
    }
    return render(request, 'lms/login.html', context)



def signup(request):
    if request.method == 'POST':
        pin = "#@Beyond_Me23"

        username = request.POST.get('userid')
        password = pin
        password2 = pin

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User ID Already Exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.is_superuser=True
                user.save()
                messages.info(request, 'Admin Added Successfully')

                #log user in and redirect to settings
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('admin-homepage')

    pagename = 'Admin Register'

    context = {
        'pagename':pagename,
    }
    return render(request, 'register.html', context)



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
