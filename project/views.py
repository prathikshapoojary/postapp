from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages
from django.http import HttpResponse
import re


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            
            # redirect_url = request.GET.get('next', 'accounts/profile')
            # return render(request, 'postlist.html')
            return redirect('/project/post/')
        else:
            messages.error(request, "Username Or Password is incorrect!",
                           extra_tags='alert alert-warning alert-dismissible fade show')

    return render(request, 'login.html')


# def logout_user(request):
#     logout(request)
#     return redirect('home')


def create_user(request):
    if request.method == 'POST':
        check1 = check2 = check3 = check4 = check5 = False
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']

            if password1 != password2:
                check1 = True
                messages.error(request, 'Password did not match!',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(username=username).exists():
                check2 = True
                messages.error(request, 'Username already exists!',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(email=email).exists():
                check3 = True
                messages.error(request, 'Email already registered!',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            # if not re.findall('\d', password1):
            #     check4 = True
            #     messages.error(request, 'Password should cantain digits!',
            #                    extra_tags='alert alert-warning alert-dismissible fade show')
            # if not re.findall('[A-Z]', password1) or re.findall('[a-z]', password1):
            #     check5 = True
            #     messages.error(request, 'Password should cantain character!',
            #                    extra_tags='alert alert-warning alert-dismissible fade show')
            
            if check1 or check2 or check3 :
                messages.error(
                    request, "Registration Failed!", extra_tags='alert alert-warning alert-dismissible fade show')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email)
                messages.success(
                    request, f'Thanks for registering {user.username}.', extra_tags='alert alert-success alert-dismissible fade show')
                return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
