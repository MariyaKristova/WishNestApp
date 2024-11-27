from django import forms
from .models import Hug

class HugForm(forms.ModelForm):
    class Meta:
        model = Hug
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add your text here...', 'maxlength': 100}),
        }
