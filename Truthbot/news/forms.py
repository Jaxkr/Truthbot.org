from django import forms
from django.core.validators import RegexValidator, URLValidator, MaxLengthValidator
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


url_validator = URLValidator()

class SubmitLink(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=350)
    link = forms.CharField(validators=[url_validator], widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=2083)
    captcha = ReCaptchaField(widget=ReCaptchaWidget())


class NewComment(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}))
