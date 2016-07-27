from django import forms

class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'editor'}))
    POSITIVE_TONE = 'P'
    NEUTRAL_TONE = 'N'
    CRITICAL_TONE = 'C'
    REVIEW_TONE_CHOICES = (
        (POSITIVE_TONE, 'Positive'),
        (NEUTRAL_TONE, 'Neutral'),
        (CRITICAL_TONE, 'Critical')
        )
    tone = forms.ChoiceField(choices=REVIEW_TONE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))