
from django.urls import path

from .views import FollowUserView, LoginView, ProfileView, RegisterView


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    path('create-profile/', ProfileView.as_view()),

    path('follow/', FollowUserView.as_view()),
]