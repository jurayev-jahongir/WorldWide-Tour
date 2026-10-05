# from django import forms
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
#
#
# class ClientRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True, label='')
#     address = forms.CharField(max_length=200, label='')
#     phone = forms.CharField(max_length=200, label='')
#
#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
#         fields = ("username", "email", "password1", "password2")

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Clients


class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='email')
    address = forms.CharField(max_length=50, label='address', required=False)
    phone = forms.CharField(max_length=50, label='phone', required=False)

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "phone", "address", "password1", "password2")