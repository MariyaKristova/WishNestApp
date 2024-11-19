from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import TemplateView, ListView, CreateView
from WishNestApp.common.forms import HugForm
from WishNestApp.common.models import Hug
from WishNestApp.events.models import Event

class HomePageView(TemplateView):
    template_name = 'common/home-page.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

class DashboardView(ListView):
    model = Event
    template_name = 'common/dashboard.html'
    context_object_name = 'events'
    ordering = ['date', 'time']
    paginate_by = 3

    def get_queryset(self):
        return Event.objects.filter(date__gte=now().date()).order_by('date', 'time')

class PastEventsView(ListView):
    model = Event
    template_name = 'common/past-events.html'
    context_object_name = 'past_events'
    ordering = ['date', 'time']
    paginate_by = 3

    def get_queryset(self):
        return Event.objects.filter(date__lt=now().date()).order_by('date', 'time')

class HugCreateView(CreateView):
    model = Hug
    form_class = HugForm
    template_name = 'common/past-events.html'
    context_object_name = 'form'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        form.instance.to_event = event
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('event-details', kwargs={'pk': self.object.to_event.pk})