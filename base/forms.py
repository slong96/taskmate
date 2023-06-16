from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Meta keeps the configuration in one place
    class Meta:
        model = User
        # order of form
        fields = ['username', 'email', 'password1', 'password2']