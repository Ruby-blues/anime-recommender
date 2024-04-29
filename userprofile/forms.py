from django import forms

from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['profile_pic', 'email', 'password1', 'password2', 'user_name', 'first_name', 'last_name', 'about']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }



