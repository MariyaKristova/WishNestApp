from django import forms

from WishNestApp.wishnests.models import Wishnest

class WishnestBaseForm(forms.ModelForm):
    class Meta:
        model = Wishnest
        fields = []

class WishnestAddForm(WishnestBaseForm):
    class Meta:
        model = Wishnest
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Add title...'}),
        }

class WishnestEditForm(WishnestBaseForm):
    pass

class WishnestDeleteForm(WishnestBaseForm):
    pass