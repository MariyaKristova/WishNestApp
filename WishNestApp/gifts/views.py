from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, FormView
from .models import Gift
from .forms import GiftAddForm, GiftEditForm, GiftDeleteForm, GiftRegistrationForm
from django.contrib import messages

class GiftAddView(LoginRequiredMixin, CreateView):
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


class GiftDetailsView(DetailView):
    model = Gift
    template_name = 'gifts/gift-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['registration_form'] = GiftRegistrationForm(user=self.request.user)
        else:
            context['registration_form'] = GiftRegistrationForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = GiftRegistrationForm(request.POST, user=request.user)
        if form.is_valid():
            self.object.is_registered = True
            self.object.registered_by_email = form.cleaned_data['email']
            self.object.save()
            messages.success(request, f"Gift successfully registered by {form.cleaned_data['email']}!")

        return redirect('wishnest-details', kwargs={'pk': self.object.wishnest.pk})


class GiftEditView(LoginRequiredMixin, UpdateView):
    model = Gift
    form_class = GiftEditForm
    template_name = 'gifts/gift-edit.html'

    def get_success_url(self):
        return reverse_lazy('gift-details', kwargs={'pk': self.object.pk})

    def test_func(self):
        gift = get_object_or_404(Gift, pk=self.kwargs['pk'])
        return self.request.user == gift.user


class GiftDeleteView(LoginRequiredMixin, DeleteView):
    model = Gift
    form_class = GiftDeleteForm
    template_name = 'gifts/gift-delete.html'

    def get_success_url(self):
        return reverse_lazy('wishnest-details', kwargs={'pk': self.object.wishnest.pk})