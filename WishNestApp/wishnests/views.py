from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView
from .models import Wishnest
from .forms import WishnestAddForm, WishnestDeleteForm
from ..events.models import Event


class WishnestAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Wishnest
    form_class = WishnestAddForm
    template_name = 'wishnests/wishnest-add.html'

    def form_valid(self, form):
        form.instance.event_id = self.kwargs['event_pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_pk'] = self.kwargs['event_pk']
        return context

    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        return self.request.user == event.user

    def get_success_url(self):
        return reverse_lazy('wishnest-details', kwargs={'pk': self.object.pk})

class WishnestDetailsView(DetailView):
    model = Wishnest
    template_name = 'wishnests/wishnest-details.html'

class WishnestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Wishnest
    form_class = WishnestDeleteForm
    template_name = 'wishnests/wishnest-delete.html'

    def test_func(self):
        wishnest = self.get_object()
        return self.request.user == wishnest.user

    def get_success_url(self):
        return reverse_lazy('event-details', kwargs={'pk': self.object.event.pk})

