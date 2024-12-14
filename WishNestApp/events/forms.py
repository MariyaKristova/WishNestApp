from django import forms
from WishNestApp.events.models import Event


class EventBaseForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['occasion', 'description', 'date', 'time', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
            }),
            'occasion': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EventCreateForm(EventBaseForm):
    pass

class EventEditForm(EventBaseForm):
    pass

class EventDeleteForm(forms.ModelForm):
    pass