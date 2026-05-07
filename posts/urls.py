from django.urls import path
from .views import PostListCreateView, PostDetailView

urlpatterns = [
    path('create-post/', PostListCreateView.as_view(), name='post-list-create'),
    path('single-post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]