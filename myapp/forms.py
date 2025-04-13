"""
forms.py

This module defines form classes for the application.
It includes forms for user login and a specialized registration form
for managers to add new users. Detailed comments are provided to explain
the purpose and function of each form and method.
"""

from django import forms
from django.contrib.auth.models import User

#############
# LoginForm #
#############
class LoginForm(forms.Form):
    """
    A simple form for user authentication.
    
    Fields:
      - username: A text field that accepts the user's username.
      - password: A password field (input masked) for the user's password.
      
    The placeholder text in the widgets is set to provide guidance on what
    information should be entered.
    """
    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )


###############################
# ManagerUserRegistrationForm #
###############################
class ManagerUserRegistrationForm(forms.Form):
    """
    A registration form for Manager users to create new user accounts.
    
    Fields:
      - username: The desired username for the new account.
      - password: The password for the new account.
      - confirm_password: A field to confirm that the user entered the correct password.
      - role: A selection field to choose the role of the new user (Manager, Technician, Repair, or View-only).
      
    Validation:
      - clean_username: Checks if the username is already taken.
      - clean: Ensures that 'password' and 'confirm_password' match.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )
    role = forms.ChoiceField(
        choices=[
            ('Manager', 'Manager'),
            ('Technician', 'Technician'),
            ('Repair', 'Repair'),
            ('View-only', 'View-only')
        ]
    )

    def clean_username(self):
        """
        Validate that the username is unique.
        If the username already exists in the system, raise a validation error.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already registered.')
        return username

    def clean(self):
        """
        Validate that the password and confirm_password fields match.
        This ensures the user has correctly entered their desired password.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
