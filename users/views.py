from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import CustomUser, Follow, SocialStats
from .serializers import FollowSerializer, FollowingListSerializer, LoginSerializer, ProfileSerializer, RegisterSerializer, SocialStatsSerializer, UserSearchSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access":  str(refresh.access_token),
    }


@api_view(['GET'])
def search_users(request):

    query = request.GET.get('q')

    if query:
        users = CustomUser.objects.filter(
    username__icontains=query
                )[:10]
    else:
        users = CustomUser.objects.none()

    serializer = UserSearchSerializer(users, many=True)

    return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [AllowAny]  # no auth needed to login

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            return Response(
                {
                    "message": "Login successful",
                    "role":    data["role"],
                    "tokens":  {
                        "access": data["access"],
                        "refresh": data["refresh"],
                    },
                },
                status=status.HTTP_200_OK,
            )

        # If validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]  # no auth needed to register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user   = serializer.save()
            tokens = get_tokens_for_user(user)

            return Response(
                {
                    "message": "Registration successful",
                    "role":    user.role,
                    "tokens":  tokens,
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            # This will show you exactly what failed
            print(serializer.errors)  # Check your terminal/console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    # create profile
    def post(self, request):

        if hasattr(request.user, 'profile'):

            return Response(
                {"error": "Profile already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response(
                {
                    "message": "Profile created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # get logged-in user's profile
    def get(self, request):

        if not hasattr(request.user, 'profile'):

            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(request.user.profile)

        return Response(serializer.data)
    
    def patch(self, request):
        if not hasattr(request.user, 'profile'):
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Profile updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllUsersView(APIView):

    permission_classes=[IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.all()
        data = [{"email": user.email, "role": user.role} for user in users]
        return Response(data, status=status.HTTP_200_OK)
    

class SocialStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ensure the user has a SocialStats record
        try:
            social_stats = request.user.social_stats
        except SocialStats.DoesNotExist:
            return Response(
                {"error": "Social stats not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SocialStatsSerializer(social_stats)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowUserView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        following_user = request.data.get('following')

        if request.user.id == int(following_user):
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Follow.objects.filter(
            follower=request.user,
            following_id=following_user
        ).exists():

            return Response(
                {'error': 'Already following this user'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = FollowSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(follower=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class FollowingListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Get all follow records
        followings = Follow.objects.filter(
            follower=request.user
        )

        # Extract users being followed
        users = [follow.following for follow in followings]

        serializer = FollowingListSerializer(users, many=True)

        return Response(serializer.data)