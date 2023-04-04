from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%d", ])
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%d", ])
    total_d = forms.IntegerField(required=True)
    total_price = forms.FloatField(required=True)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]
