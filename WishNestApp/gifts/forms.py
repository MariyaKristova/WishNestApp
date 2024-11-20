from django import forms
from WishNestApp.gifts.models import Gift

class GiftBaseForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ['image', 'description', 'price', 'url']

class GiftAddForm(GiftBaseForm):
    pass

class GiftEditForm(GiftBaseForm):
    pass

class GiftDeleteForm(GiftBaseForm):
    pass

class GiftRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, label="Enter your name...")
