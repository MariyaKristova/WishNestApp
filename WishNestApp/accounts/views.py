from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from WishNestApp.accounts.forms import UserCreateForm, ProfileEditForm
from WishNestApp.accounts.models import Profile

UserModel = get_user_model()

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

class RegisterView(CreateView):
    model = UserModel
    form_class = UserCreateForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name='accounts/profile-edit.html'

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={'pk': self.object.pk}
        )


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

        # photos_with_likes = self.object.photo_set.annotate(likes_count=Count('like'))
        # context['total_likes_count'] = sum(photo.likes_count for photo in photos_with_likes)
        # context['total_pets_count'] = self.object.pet_set.count()
        # context['total_photos_count'] = self.object.photo_set.count()

        # return context

class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user