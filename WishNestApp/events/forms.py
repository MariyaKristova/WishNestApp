from django import forms
from django.utils import timezone
from WishNestApp.events.models import Event


class EventBaseForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['occasion', 'description', 'date', 'time', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class EventCreateForm(EventBaseForm):
    pass

class EventEditForm(EventBaseForm):
    pass

class EventDeleteForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['occasion', 'description', 'date', 'time', 'location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['readonly'] = 'readonly'




