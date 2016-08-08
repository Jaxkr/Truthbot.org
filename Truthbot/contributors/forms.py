from django import forms

class EditBio(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 300}))
