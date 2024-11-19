from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import TemplateView, ListView, CreateView

from WishNestApp.accounts.models import Profile
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hug_form'] = HugForm()
        return context

class HugCreateView(CreateView):
    model = Hug
    form_class = HugForm
    template_name = 'common/past-events.html'
    context_object_name = 'form'
    success_url = reverse_lazy('past-events')

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        form.instance.to_event = event

        # if self.request.user.is_authenticated:
        #     try:
        #         profile = self.request.user.profile
        #         form.instance.name = profile.first_name
        #     except Profile.DoesNotExist:
        #         form.add_error('name', 'Profile information not found.')
        #         return self.form_invalid(form)
        # else:
        #     if not form.instance.name:
        #         form.add_error('name', 'Please provide your name.')
        #         return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return context