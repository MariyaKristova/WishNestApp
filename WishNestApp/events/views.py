from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages

from WishNestApp.events.forms import EventBaseForm, EventDetailsForm, EventEditForm, EventDeleteForm
from WishNestApp.events.models import Event


class EventCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'events/event-create.html'
    form_class = EventBaseForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.host = self.request.user
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'events/event-details.html'
    context_object_name = 'event'
    form_class = EventDetailsForm

class EventEditView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Event
    template_name = 'events/event-edit.html'
    form_class = EventEditForm
    context_object_name = 'event'

    def get_success_url(self):
        return reverse_lazy('event-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.host

    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully!')
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this event.")
        return super().handle_no_permission()


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Event
    template_name = 'events/event-delete.html'
    success_url = reverse_lazy('event-list')
    form_class = EventDeleteForm
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.get_object())
        return context

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.host

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Event deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete this event.")
        return super().handle_no_permission()
