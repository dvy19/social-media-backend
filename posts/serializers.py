from rest_framework import serializers
from .models import Post

from django.contrib.auth import get_user_model
User = get_user_model()


class PostUserSerializer(serializers.ModelSerializer):

    city = serializers.CharField(
        source="profile.city",
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "city"
        ]

class PostSerializer(serializers.ModelSerializer):

    user = PostUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'title',
            'content',
            'category',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'id',
            'user',
            'created_at',
            'updated_at'
        ]