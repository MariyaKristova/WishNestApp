from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/', include([
        path('', views.EventDetailView.as_view(), name='event-details'),
        path('edit/', views.EventEditView.as_view(), name='event-edit'),
        path('delete/', views.EventDeleteView.as_view(), name='event-delete'),
    ])),
]