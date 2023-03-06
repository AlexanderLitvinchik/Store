from django.urls import path
from .views import login, logout, registration, profile, UserProfileView, UserRegistrationView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),

    # path('profile/', profile, name='profile'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', logout, name='logout')
]
