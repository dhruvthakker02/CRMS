from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.db import transaction
from django.core.validators import MinLengthValidator,EmailValidator


class TenantRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[MinLengthValidator(limit_value=1, message="First name cannot be empty.")]
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[MinLengthValidator(limit_value=1, message="Last name cannot be empty.")]
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        },
        validators=[EmailValidator(message="Enter a valid email address.")]
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'id_proof', 'state', 'city', 'area', 'contact']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tenant = True
        user.save()
        return user

class RenterRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[MinLengthValidator(limit_value=1, message="First name cannot be empty.")]
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[MinLengthValidator(limit_value=1, message="Last name cannot be empty.")]
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        },
        validators=[EmailValidator(message="Enter a valid email address.")]
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'id_proof', 'state', 'city', 'area', 'contact']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_renter = True
        user.save()
        return user

# def __init__(self, *args, **kwargs):
#         super(TenantRegistrationForm, self).__init__(*args, **kwargs)

#         # Check if the user is a renter, and adjust fields accordingly
#         if self.instance.is_renter:
#             # Show only renter-related fields
#             self.fields['renter_specific_field'] = forms.CharField(label='Renter Specific Field')

  
    
    

