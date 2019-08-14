from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Photographer


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class Connection_form(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Photographer
        fields = ['image']

        widgets = {
          'image': forms.FileInput(attrs={'class': 'color-green'}),
        }
