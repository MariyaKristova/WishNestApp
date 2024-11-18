from django import forms

from WishNestApp.wishnests.models import Wishnest

class WishnestBaseForm(forms.ModelForm):
    class Meta:
        model = Wishnest
        fields = ['event']

class WishnestAddForm(WishnestBaseForm):
    pass

class WishnestEditForm(WishnestBaseForm):
    pass

class WishnestDeleteForm(WishnestBaseForm):
    pass