from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages

from WishNestApp.events.forms import EventEditForm, EventDeleteForm, EventCreateForm
from WishNestApp.events.models import Event


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'events/event-create.html'
    form_class = EventCreateForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'events/event-details.html'
    context_object_name = 'event'

class EventEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Event
    template_name = 'events/event-edit.html'
    form_class = EventEditForm
    context_object_name = 'event'

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.host

    def get_success_url(self):
        return reverse_lazy('event-detail', kwargs={'pk': self.object.pk})


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Event
    template_name = 'events/event-delete.html'
    success_url = reverse_lazy('dashboard')
    form_class = EventDeleteForm

    def get_initial(self) -> dict:
        return self.get_object().__dict__

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.host
