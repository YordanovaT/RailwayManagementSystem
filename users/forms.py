from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    """Creating a form, which will be used for user registration"""

    email = forms.EmailField(max_length=150, help_text='Required. Please add valid email address')

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")


class UserLogInForm(forms.ModelForm):
    """Creating a form, which will be used for user log in"""

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login.")
