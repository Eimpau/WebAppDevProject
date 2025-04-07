from django import forms
from django.contrib.auth.models import User

# This form is used for user login
# It has fields for username and password
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
