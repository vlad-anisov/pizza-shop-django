from django import forms
from .models import Address
from django.contrib.auth.models import User


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
