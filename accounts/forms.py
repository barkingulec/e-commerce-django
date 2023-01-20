from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={
        'class': 'input-line',
        'placeholder': 'Username',
        }))
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'class': 'input-line',
        'placeholder': 'Password',
        }))

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={
        'class': 'input-line',
        'placeholder': 'Username',
        }))
    email = forms.CharField(widget = forms.EmailInput(attrs={
        'class': 'input-line',
        'placeholder': 'Email',
        }))
    password1 = forms.CharField(widget = forms.PasswordInput(attrs={
        'class': 'input-line',
        'placeholder': 'Password',
        }))
    password2 = forms.CharField(widget = forms.PasswordInput(attrs={
        'class': 'input-line',
        'placeholder': 'Re-type Password',
        }))
    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']