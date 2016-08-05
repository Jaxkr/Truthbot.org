from django import forms
from django.core.validators import RegexValidator, URLValidator, MaxLengthValidator

url_validator = URLValidator()

class SubmitLink(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=350)
    link = forms.CharField(validators=[url_validator], widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=2083)
