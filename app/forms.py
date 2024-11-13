from django import forms
from . import models 


class SubscribeForm(forms.Form):
   
    email = forms.EmailField()


class registerForm(forms.ModelForm):

    pass