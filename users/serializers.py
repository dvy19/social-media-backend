
from datetime import date

from rest_framework import serializers
from .models import CustomUser, Follow, Profile, SocialStats

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):

    # write_only = password will never be sent back in response
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = CustomUser
        fields = ["email", "password", "role"]

    def create(self, validated_data):
        # Use our custom manager to create the user
        user = CustomUser.objects.create_user(
            email    = validated_data["email"],
            password = validated_data["password"],
            role     = validated_data["role"],
        )
        return user
    

class LoginSerializer(serializers.Serializer):

    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role
        }
    

class SocialStatsSerializer(serializers.ModelSerializer):

    followers_count = serializers.IntegerField(source="followers_count", read_only=True)
    following_count = serializers.IntegerField(source="following_count", read_only=True)
    posts_count = serializers.IntegerField(source="posts_count", read_only=True)

    class Meta:
        model = SocialStats
        fields = ["followers_count", "following_count", "posts_count"]

        
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    social_stats = SocialStatsSerializer(source="user.social_stats", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id", "first_name", "last_name", "city", "gender",
            "date_of_birth", "bio", "user", "created_at", "updated_at",
            "social_stats"
        ]
        read_only_fields = ["user", "created_at", "updated_at"]


    def validate_date_of_birth(self, value):
        if value and value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

class FollowSerializer(serializers.ModelSerializer):

    follower = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'follower', 'created_at']

