from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.GiftAddView.as_view(), name='gift-add'),
    path('gift/<int:pk>/', include([
        path('', views.GiftDetailsView.as_view(), name='gift-details'),
        path('edit/', views.GiftEditView.as_view(), name='gift-edit'),
        path('delete/', views.GiftDeleteView.as_view(), name='gift-delete'),
    ])),
]