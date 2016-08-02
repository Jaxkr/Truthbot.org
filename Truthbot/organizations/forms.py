from django import forms
from django.core.validators import RegexValidator, URLValidator, MaxLengthValidator

url_validator = URLValidator()

class OrganizationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=300)
    description = forms.CharField(validators=[MaxLengthValidator(1000)], widget=forms.Textarea(attrs={'class': 'form-control'}), max_length=1000)
    homepage = forms.CharField(validators=[url_validator], widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=2083)

valid_domain_validator = RegexValidator('^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$', 'The input must be a valid domain.')
class AddDomain(forms.Form):
    domain = forms.CharField(validators=[valid_domain_validator], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg. "google.com"'}), max_length=150)

class OrganizationSearch(forms.Form):
    search_term = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Start of organization name...', 'style': 'height: 50px;font-size: 20px'}), max_length=50)

class OrganizationWikiForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'editor', 'rows': 16}))
