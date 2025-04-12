from django import forms
from django.contrib.auth.models import User

# This form is used for user login
# It has fields for username and password
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})) # Placeholder text in input field
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})) # Field for entering password

# This form is used to register a new user with a specific role
class ManagerUserRegistrationForm(forms.Form):
    username = forms.CharField( # Field for entering username
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}) # Placeholder text
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    confirm_password = forms.CharField( # Confirm password field to double-check password match
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )
    role = forms.ChoiceField(choices=[('Manager', 'Manager'), ('Technician', 'Technician'),('Repair', 'Repair'), ('View', 'View')]  # Role selection field with predefined choices
    )

# Custom validation to check if the username already exists
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already registered.')
        return username

# Check if both password fields are present and match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
