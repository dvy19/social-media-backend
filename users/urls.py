
from django.urls import path

from .views import FollowUserView, FollowingListView, LoginView, ProfileView, RegisterView, SocialStatsView, search_users


urlpatterns = [
    path('search-users/', search_users),

    path("register/", RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    path('create-profile/', ProfileView.as_view()),

    path('follow/', FollowUserView.as_view()),

    path('social-stats/',SocialStatsView.as_view()),

    path('following/', FollowingListView.as_view())
]