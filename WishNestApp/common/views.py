from django.views.generic import TemplateView, ListView

class HomePageView(TemplateView):
    template_name = 'common/home-page.html'

# class DashboardView(ListView):
#     model = Event
#     template_name = 'dashboard.html'
#     context_object_name = 'events'


