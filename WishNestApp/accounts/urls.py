from django.contrib.auth.views import LogoutView
from django.urls import path, include
from WishNestApp.accounts.views import RegisterView, UserLoginView, ProfileDetailView, ProfileEditView, \
    ProfileDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', ProfileDetailView.as_view(), name='profile-details'),
        path('edit/', ProfileEditView.as_view(), name='profile-edit'),
        path('delete', ProfileDeleteView.as_view(), name='profile-delete'),
    ])),
]