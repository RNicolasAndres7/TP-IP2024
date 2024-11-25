from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms



class registerForm(UserCreationForm):

    usable_password = None

    class Meta:

        model = User

        fields = ["username", "password1", "password2"]

