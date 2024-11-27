from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from WishNestApp.common.forms import HugForm
from WishNestApp.common.models import ShareLink
from WishNestApp.events.forms import EventEditForm, EventDeleteForm, EventCreateForm
from WishNestApp.events.models import Event


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventCreateForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'events/event-details.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hug_form'] = HugForm()

        if self.request.user == self.object.user:
            share_link = ShareLink.objects.filter(event=self.object, expires_at__gt=timezone.now()).first()
            if not share_link:
                share_link = ShareLink.objects.create(event=self.object, expires_at=self.object.date + timedelta(days=7))

            current_site = get_current_site(self.request)
            share_url = f"https://{current_site.domain}{reverse('shared-event', kwargs={'token': share_link.token})}"
            context['share_url'] = share_url

        return context

class EventEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Event
    template_name = 'events/event-edit.html'
    form_class = EventEditForm
    context_object_name = 'event'

    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return self.request.user == event.user

    def get_success_url(self):
        return reverse_lazy('event-details', kwargs={'pk': self.object.pk})

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Event
    template_name = 'events/event-delete.html'
    success_url = reverse_lazy('dashboard')
    form_class = EventDeleteForm

    def get_initial(self) -> dict:
        return self.get_object().__dict__

    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return self.request.user == event.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'data': self.get_initial(),})

        return kwargs
