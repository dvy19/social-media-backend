from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):

    user=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Post
        fields=['id', 'user', 'title', 'content', 'category', 'created_at', 'updated_at']

        read_only_fields=['id', 'user', 'created_at', 'updated_at']
        