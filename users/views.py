""" Views for Users application."""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLogInForm


# Create your views here.


def user_registration(request):
    """
        This function is used for user registration.
        Args:
            request: Http request
        Returns:
    """

    context = {}
    if request.POST:
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            email = register_form.cleaned_data.get('email')
            password1 = register_form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password1)
            login(request, user)
            context['success'] = True

            return redirect('index')

        context['register_form'] = register_form
    else:
        register_form = UserRegistrationForm()
        context['register_form'] = register_form
    return render(request, 'users/register.html', context)


def login_view(request):
    """
        This function is used for logging in user.
        Args:
            request: Http request
        Returns:
    """

    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('index')
    if request.POST:
        login_form = UserLogInForm(request.POST)
        if login_form.is_valid():

            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('index')
    else:
        login_form = UserLogInForm()
    context['login_form'] = login_form
    return render(request, 'users/login.html', context)


def user_logout(request):
    """
        This function is used for logging out user.
        Args:
            request: Http request
        Returns:
    """

    logout(request)
    return redirect('index')
