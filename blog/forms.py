# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email/Phone',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email или телефон'}),
        max_length=254
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )

class RegisterCashierForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    
from django import forms
from .models import Reviews

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['name', 'review_text', 'photo']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4}),
        }
