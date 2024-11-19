from django.urls import path
from . import views
from .views import HugCreateView

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('past_events/', views.PastEventsView.as_view(), name='past-events'),
    path('hug/<int:event_id>/', HugCreateView.as_view(), name='hug'),
]