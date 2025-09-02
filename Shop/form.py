from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields
        for field_name in self.fields:
            if field_name == 'username':
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Enter your username'
                })
            elif field_name == 'password1':
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Enter your password'
                })
            elif field_name == 'password2':
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': 'Confirm your password'
                })
            else:
                # For other fields that might not have been explicitly set
                if 'class' not in self.fields[field_name].widget.attrs:
                    self.fields[field_name].widget.attrs.update({
                        'class': 'form-control'
                    })
