from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'form-control',
            'title': 'Username can not be blank, must be unique.',
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'First Name',
            'class': 'form-control',
            'title': 'First name can not be blank.',
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Last Name',
            'class': 'form-control',
            'title': 'Last name can not be blank.',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email',
            'class': 'form-control',
            'title': 'Email must be valid.',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control',
            'title': 'At least 8 characters, not entirely numeric, not too common.',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control',
            'title': 'Re-enter your password for confirmation.',
        })

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'bio', 'birthday', 'location']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }