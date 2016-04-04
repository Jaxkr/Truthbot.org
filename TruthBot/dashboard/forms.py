from django import forms
from django.core.validators import RegexValidator, URLValidator

url_validator = URLValidator()

class NewOrganization(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=300)
	logo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
	info_url = forms.CharField(validators=[url_validator], widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=2083)

valid_domain_validator = RegexValidator('^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$', 'The input must be a valid domain.')
class AddDomain(forms.Form):
	domain = forms.CharField(validators = [valid_domain_validator], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg. "google.com"'}), max_length=150)