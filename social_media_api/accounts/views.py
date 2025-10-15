from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, UserProfileSerializer, UserFollowSerializer

CustomUser = get_user_model()

# Authentication Views
class RegisterView(generics.GenericAPIView):
    """View for user registration"""
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    """View for user login"""
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

# Follow/Unfollow Views
class FollowUserView(generics.GenericAPIView):
    """View to follow a user"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserFollowSerializer
    
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        
        # Prevent users from following themselves
        if user_to_follow == request.user:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Follow the user
        if request.user.follow(user_to_follow):
            return Response(
                {"message": f"You are now following {user_to_follow.username}"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": f"You are already following {user_to_follow.username}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class UnfollowUserView(generics.GenericAPIView):
    """View to unfollow a user"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserFollowSerializer
    
    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        
        # Unfollow the user
        if request.user.unfollow(user_to_unfollow):
            return Response(
                {"message": f"You have unfollowed {user_to_unfollow.username}"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": f"You are not following {user_to_unfollow.username}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(generics.RetrieveAPIView):
    """View to get user profile with follow status"""
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        return get_object_or_404(CustomUser, id=self.kwargs['user_id'])

class UserFollowersView(generics.ListAPIView):
    """View to get a user's followers"""
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        return user.followers.all()

class UserFollowingView(generics.ListAPIView):
    """View to get users that a user is following"""
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        return user.following.all()

# Current user profile
class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    """View to get and update current user's profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user