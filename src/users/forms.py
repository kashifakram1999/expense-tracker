from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    currency = forms.CharField(max_length=3, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'currency', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('monthly_budget', 'default_category')