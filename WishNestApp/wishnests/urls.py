from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.WishnestAddView.as_view(), name='wishnest-add'),
    path('wishnest/<int:pk>/', include([
        path('', views.WishnestDetailsView.as_view(), name='wishnest-details'),
        path('edit/', views.WishnestEditView.as_view(), name='wishnest-edit'),

        path('delete/', views.WishnestDeleteView.as_view(), name='wishnest-delete'),
    ])),
]