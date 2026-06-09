from django.urls import path
from .views import PostListCreateView, PostDetailView, toggle_like

urlpatterns = [
    path('create-post/', PostListCreateView.as_view(), name='post-list-create'),
    path('single-post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

     path(
        'like-post/<int:post_id>/like/',
        toggle_like,
        name='toggle_like'
    ),
]