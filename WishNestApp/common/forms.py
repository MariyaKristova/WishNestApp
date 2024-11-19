from django import forms
from .models import Hug

class HugForm(forms.ModelForm):
    class Meta:
        model = Hug
        exclude = ['to_event']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add your text here...'}),
        }
