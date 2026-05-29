
from django.urls import path
from flask import views

from .views import FollowUserView, FollowingListView, LoginView, ProfileView, RegisterView, SocialStatsView, UserProfileView, search_users


urlpatterns = [
    path('search-users/', search_users),

    path("register/", RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    path('create-profile/', ProfileView.as_view()),

    path('friend-profile/<int:id>/', UserProfileView.as_view(), name='user-profile'),


    path('follow/', FollowUserView.as_view()),

    path('social-stats/',SocialStatsView.as_view()),

    path('following/', FollowingListView.as_view())
]