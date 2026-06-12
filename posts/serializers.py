from rest_framework import serializers
from .models import Post

from django.contrib.auth import get_user_model
User = get_user_model()



class PostUserSerializer(serializers.ModelSerializer):


    first_name = serializers.CharField(
        source="profile.first_name",
        read_only=True
    )

    last_name = serializers.CharField(
        source="profile.last_name",
        read_only=True
    )

    city = serializers.CharField(
        source="profile.city",
        read_only=True
    )

    class Meta:
        model =User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "city"
        ]


class PostSerializer(serializers.ModelSerializer):

    user = PostUserSerializer(read_only=True)

    likes_count = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'title',
            'content',
            'category',
            'likes_count',
            'created_at',
            'updated_at'
        ]

        read_only_fields = [
            'id',
            'user',
            'likes_count',
            'created_at',
            'updated_at'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()