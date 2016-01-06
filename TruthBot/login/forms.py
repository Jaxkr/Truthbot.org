from django import forms
from django.utils.html import escape, strip_tags
from django.core.validators import RegexValidator

#nonform classes
class BSCharField(forms.CharField):
    def widget_attrs(self, widget):
        attrs = super(BSCharField, self).widget_attrs(widget)
        attrs.update({'class':'form-control'})
        if self.max_length is not None and isinstance(widget, (forms.TextInput, forms.HiddenInput)):
            # The HTML attribute is maxlength, not max_length.
            attrs.update({'maxlength': str(self.max_length)})
        return attrs

#auth forms
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
class RegistrationForm(forms.Form):
    username = BSCharField(validators = [alphanumeric], max_length=24, widget=forms.TextInput(attrs={'placeholder': 'Your desired username.'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Your email.'}))
    password1 = BSCharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Desired password. Make it strong!'}))
    password2 = BSCharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password for verification.'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

class LoginForm(forms.Form):
    username = BSCharField(validators = [alphanumeric], max_length=24, widget=forms.TextInput(attrs={'placeholder': 'Your username'}))
    password = BSCharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))
