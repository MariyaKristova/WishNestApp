from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm

from WishNestApp.accounts.models import Profile

UserModel = get_user_model()

class UserEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel

class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        labels = {
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'profile_picture': 'Profile Picture:',
        }