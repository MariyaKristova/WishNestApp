from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import TemplateView, ListView, CreateView
from WishNestApp.common.forms import HugForm
from WishNestApp.common.models import Hug, ShareLink
from WishNestApp.events.models import Event
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

class HomePageView(TemplateView):
    template_name = 'common/home-page.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'common/dashboard.html'
    context_object_name = 'events'
    ordering = ['date', 'time']
    paginate_by = 3

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user).filter(date__gte=now().date()).order_by('date', 'time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = "Upcoming Events"
        context['show_subheader'] = False
        return context


class PastEventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'common/dashboard.html'
    context_object_name = 'events'
    ordering = ['date', 'time']
    paginate_by = 3

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user).filter(date__lt=now().date()).order_by('date', 'time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = "Past Events"
        context['show_subheader'] = True
        context['subheader'] = "Send hugs & kisses to your guests! Past events are saved for a week."
        return context

class HugCreateView(CreateView):
    model = Hug
    form_class = HugForm
    template_name = 'common/dashboard.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return context

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        form.instance.author = self.request.user
        form.instance.to_event = event
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event-details', kwargs={'pk': self.object.to_event.pk})


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)

class SharedEventView(View):
    def get(self, request, token):
        try:
            share_link = ShareLink.objects.get(token=token)
            if share_link.is_valid():
                return redirect('event-details', pk=share_link.event.pk)
            else:
                raise Http404
        except ShareLink.DoesNotExist:
            raise Http404