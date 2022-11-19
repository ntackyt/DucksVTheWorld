"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    email = forms.EmailField(max_length=254,label=_('Email'),
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))
    test = forms.IntegerField()
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    


class BootstrapRegisterForm(UserCreationForm):
     email = forms.EmailField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))
     first_name = forms.CharField(max_length=254,
                                 label=_("First name"),
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'First name'}))
     last_name = forms.CharField(max_length=254,
                               label=_("Last name"),
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Last name'}))
     password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
     password2 = forms.CharField(label=_("Confirm Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Confirm Password'}))
