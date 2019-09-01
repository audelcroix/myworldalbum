from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from .models import Photographer


class UserRegisterForm(UserCreationForm):

    # /!\ the * symbol on labels is from crispy forms and named asteriskField

    username = forms.CharField(label="Username ", help_text="Choose your photographer name")
    email = forms.EmailField(label="Email ")
    password1 = forms.CharField(
        label="Password ",
        widget=forms.PasswordInput,
        help_text=mark_safe("Choose carefully<br>Must contain at least 8 characters<br>Must not be only digits")
    )

    password2 = forms.CharField(
        label="Password confirmation ",
        widget=forms.PasswordInput,
        help_text="Please type again for verification"
    )

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


class PasswordUpdateForm(forms.Form):
    old_password = forms.CharField(
        label="Current password ",
        widget=forms.PasswordInput,
        help_text="Enter your current password"
    )
    new_password = forms.CharField(
        label="New password ",
        widget=forms.PasswordInput,
        help_text=mark_safe("Choose carefully<br>Must contain at least 8 characters<br>Must not be only digits")
    )
    new_password_conf = forms.CharField(
        label="Repeat new password ",
        widget=forms.PasswordInput,
        help_text="Type your new password again"
    )


    def clean(self):
        cleaned_data = super(PasswordUpdateForm, self).clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        new_password_conf = cleaned_data.get('new_password_conf')

        if old_password == new_password:
            raise forms.ValidationError(
                "New password can't be the same as old password"
            )

        if new_password_conf != new_password:
            raise forms.ValidationError(
                "New password confirmation doesn't match"
            )

        return cleaned_data
