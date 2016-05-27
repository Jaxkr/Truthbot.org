from django import forms
from django.utils.html import escape, strip_tags
from django.core.validators import RegexValidator


#auth forms
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
class RegistrationForm(forms.Form):
    username = forms.CharField(validators = [alphanumeric], max_length=24, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your desired username.'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Your email.'}))
    password1 = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Desired password. Make it strong!'}))
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat password for verification.'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(validators = [alphanumeric], max_length=24, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your username'}))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your password'}))
