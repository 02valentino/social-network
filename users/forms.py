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
        fields = ['profile_picture', 'first_name', 'last_name', 'bio', 'birthday', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_picture'].widget.clear_checkbox_label = ''
        if hasattr(self.fields['profile_picture'].widget, 'template_name'):
            self.fields['profile_picture'].widget.template_name = 'django/forms/widgets/file.html'