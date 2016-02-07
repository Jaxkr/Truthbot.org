from django import forms
from django.core.validators import RegexValidator, URLValidator

url_validator = URLValidator()

class NewOrganization(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=300)
	logo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
	info_url = forms.CharField(validators=[url_validator], widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=2083)