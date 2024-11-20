from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .models import Wishnest
from .forms import WishnestAddForm, WishnestEditForm, WishnestDeleteForm

class WishnestAddView(LoginRequiredMixin, CreateView):
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

    def get_success_url(self):
        return reverse_lazy('wishnest-details', kwargs={'pk': self.object.pk})

class WishnestDetailsView(DetailView):
    model = Wishnest
    template_name = 'wishnests/wishnest-details.html'

class WishnestEditView(LoginRequiredMixin, UpdateView):
    model = Wishnest
    form_class = WishnestEditForm
    template_name = 'wishnests/wishnest-edit.html'

    def test_func(self):
        event = get_object_or_404(Wishnest, pk=self.kwargs['pk'])
        return self.request.user == event.user

    def get_success_url(self):
        return reverse_lazy('wishnest-details', kwargs={'pk': self.object.pk})

class WishnestDeleteView(LoginRequiredMixin, DeleteView):
    model = Wishnest
    form_class = WishnestDeleteForm
    template_name = 'wishnests/wishnest-delete.html'

    def get_success_url(self):
        return reverse_lazy('event-details', kwargs={'pk': self.object.event.pk})
