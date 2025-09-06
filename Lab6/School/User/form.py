from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()

class RegisterForm(UserCreationForm):
    password1=forms.CharField(label="password",widget=forms.PasswordInput())
    password2=forms.CharField(label="Confirm password",widget=forms.PasswordInput())
    class Meta:
        model = get_user_model()
        fields = ['username','email','password1','password2']
        widgets={
            'username':forms.TextInput(),
            'email':forms.EmailInput(),
        }