from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('past_events/', views.PastEventsView.as_view(), name='past-events'),
]