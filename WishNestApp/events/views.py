from datetime import timedelta
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.sites.shortcuts import get_current_site
from WishNestApp.common.forms import HugForm
from WishNestApp.common.models import ShareLink
from WishNestApp.events.forms import EventEditForm, EventDeleteForm, EventCreateForm
from WishNestApp.events.models import Event


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventCreateForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event-details.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hug_form'] = HugForm()

        if self.request.user == self.object.user:
            share_link = ShareLink.objects.filter(event=self.object, expires_at__gt=now()).first()
            if not share_link:
                share_link = ShareLink.objects.create(
                    event=self.object,
                    expires_at=self.object.date + timedelta(days=7)
                )

            token_path = reverse('shared-event', kwargs={'token': share_link.token})
            if self.request.get_host() == 'localhost:8000':
                share_url = f"http://{self.request.get_host()}{token_path}"
            else:
                current_site = get_current_site(self.request)
                share_url = f"https://{current_site.domain}{token_path}"

            context['share_url'] = share_url

        return context

class EventEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    template_name = 'events/event-edit.html'
    form_class = EventEditForm
    context_object_name = 'event'

    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        if self.request.user.is_superuser or self.request.user.has_perm('events.change_event'):
            return True
        if self.request.user == event.user and not event.is_past:
            return True

        return False

    def get_success_url(self):
        return reverse_lazy('event-details', kwargs={'pk': self.object.pk})

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event-delete.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return self.request.user.is_superuser or self.request.user.has_perm('events.delete_event') or self.request.user == event.user
