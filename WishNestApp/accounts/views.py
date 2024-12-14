from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from WishNestApp.accounts.forms import UserCreateForm, ProfileEditForm
from WishNestApp.accounts.models import Profile

UserModel = get_user_model()

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('dashboard'))
        return super().dispatch(request, *args, **kwargs)

class RegisterView(CreateView):
    model = UserModel
    form_class = UserCreateForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            login(self.request, self.object)
            return response
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('dashboard'))
        return super().dispatch(request, *args, **kwargs)

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name='accounts/profile-edit.html'

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return (self.request.user.is_superuser
                or self.request.user.has_perm('accounts.change_profile')
                or self.request.user == profile.user)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})


class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return (self.request.user.is_superuser
                or self.request.user.has_perm('accounts.view_profile')
                or self.request.user == profile.user)

class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('home-page')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return (self.request.user.is_superuser
                or self.request.user.has_perm('accounts.delete_profile')
                or self.request.user == profile.user)

    def delete(self, request, *args, **kwargs):
        user = self.get_object().user
        response = super().delete(request, *args, **kwargs)
        user.delete()
        return response