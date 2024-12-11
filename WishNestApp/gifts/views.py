from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, FormView
from .models import Gift
from .forms import GiftAddForm, GiftEditForm, GiftDeleteForm, GiftRegistrationForm
from django.contrib import messages

from ..wishnests.models import Wishnest


class GiftAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Gift
    form_class = GiftAddForm
    template_name = 'gifts/gift-add.html'

    def form_valid(self, form):
        form.instance.wishnest_id = self.kwargs['wishnest_pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishnest_pk'] = self.kwargs['wishnest_pk']
        return context

    def get_success_url(self):
        return reverse_lazy('wishnest-details', kwargs={'pk': self.object.wishnest.pk})

    def test_func(self):
        wishnest = get_object_or_404(Wishnest, pk=self.kwargs['wishnest_pk'])
        return self.request.user.is_superuser or self.request.user.has_perm('gifts.add_gift') or self.request.user == wishnest.user


class GiftDetailsView(DetailView, FormView):
    model = Gift
    template_name = 'gifts/gift-details.html'
    form_class = GiftRegistrationForm

    def form_valid(self, form):
        gift = self.get_object()
        if gift.is_registered:
            return redirect(self.get_success_url())
        gift.is_registered = True
        gift.registered_by_email = self.request.user.email
        gift.save()
        return super().form_valid(form)

    def get_success_url(self):
        gift = self.get_object()
        return reverse_lazy('wishnest-details', kwargs={'pk': gift.wishnest.pk})


class GiftEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Gift
    form_class = GiftEditForm
    template_name = 'gifts/gift-edit.html'

    def get_success_url(self):
        return reverse_lazy('gift-details', kwargs={'pk': self.object.pk})

    def test_func(self):
        gift = get_object_or_404(Gift, pk=self.kwargs['pk'])
        if self.request.user.has_perm('gifts.change_gift') or self.request.user.is_superuser:
            return True
        if self.request.user == gift.user and not gift.is_registered:
            return True
        return False

class GiftDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Gift
    form_class = GiftDeleteForm
    template_name = 'gifts/gift-delete.html'

    def get_success_url(self):
        return reverse_lazy('wishnest-details', kwargs={'pk': self.object.wishnest.pk})

    def test_func(self):
        gift = get_object_or_404(Gift, pk=self.kwargs['pk'])
        return self.request.user.is_superuser or self.request.user.has_perm('gifts.delete_gift') or self.request.user == gift.user