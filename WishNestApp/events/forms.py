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
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            event_datetime = timezone.datetime.combine(date, time)
            if event_datetime < timezone.now():
                raise forms.ValidationError("Event date and time cannot be in the past!")

        return cleaned_data


class EventEditForm(EventBaseForm):
    class Meta(EventBaseForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['occasion'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update({'class': 'form-control'})


class EventDetailsForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['occasion', 'description', 'date', 'time', 'location']


class EventDeleteForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

        widgets = {
            'occasion': forms.TextInput(attrs={'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'readonly': 'readonly', 'rows': 4}),
            'date': forms.DateInput(attrs={'readonly': 'readonly'}),
            'time': forms.TimeInput(attrs={'readonly': 'readonly'}),
            'location': forms.TextInput(attrs={'readonly': 'readonly'}),
        }




