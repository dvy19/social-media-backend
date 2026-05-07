from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer


class PostListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # get all posts
    def get(self, request):

        # get category from URL
        category = request.query_params.get('category')

        # if category exists
        if category:
            posts = Post.objects.filter(category=category).order_by('-created_at')

        # otherwise return all posts
        else:
            posts = Post.objects.all().order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # create new post
    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)   # attach logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# single posts view, update, delete
class PostDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_object(pk)

        if not post:
            return Response({'error': 'Post not found'}, status=404)

        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)

        if not post:
            return Response({'error': 'Post not found'}, status=404)

        # 🔐 Only owner can update
        if post.user != request.user:
            return Response({'error': 'Not allowed'}, status=403)

        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()   # user already exists
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        post = self.get_object(pk)

        if not post:
            return Response({'error': 'Post not found'}, status=404)

        # 🔐 Only owner can delete
        if post.user != request.user:
            return Response({'error': 'Not allowed'}, status=403)

        post.delete()
        return Response({'message': 'Post deleted'}, status=204)