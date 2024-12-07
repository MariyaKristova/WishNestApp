from django.urls import path, include
from . import views

urlpatterns = [
    path('event/<int:event_pk>/add/', views.WishnestAddView.as_view(), name='wishnest-add'),
    path('wishnest/<int:pk>/', include([
        path('', views.WishnestDetailsView.as_view(), name='wishnest-details'),
        path('delete/', views.WishnestDeleteView.as_view(), name='wishnest-delete'),
    ])),
]