from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from WishNestApp.accounts.models import Profile

UserModel = get_user_model()

class UserEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel

class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


    def clean_email(self):
        email = self.cleaned_data['email']
        email = UserModel.objects.normalize_email(email) #fix: DRY

        if UserModel.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        labels = {
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'profile_image': 'Add New Image:',
        }

        widgets = {
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
            })
        }