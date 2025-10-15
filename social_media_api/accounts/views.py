from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Get the token that was created in the serializer
        token = Token.objects.get(user=user)
        
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    token = Token.objects.get(user=user)
    
    return Response({
        'user': UserSerializer(user).data,
        'token': token.key,
        'message': 'Login successful'
    })

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != user_to_follow and not request.user.following.filter(id=user_id).exists():
        request.user.following.add(user_to_follow)
        return Response({'message': f'You are now following {user_to_follow.username}'})
    else:
        return Response({'error': 'Unable to follow user'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user.following.filter(id=user_id).exists():
        request.user.following.remove(user_to_unfollow)
        return Response({'message': f'You have unfollowed {user_to_unfollow.username}'})
    else:
        return Response({'error': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user
    """
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user.id == user_id:
        return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.user.follow(user_to_follow):
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'following': True,
            'followers_count': user_to_follow.followers_count
        })
    else:
        return Response({
            'error': 'You are already following this user',
            'following': True
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user
    """
    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user.unfollow(user_to_unfollow):
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'following': False,
            'followers_count': user_to_unfollow.followers_count
        })
    else:
        return Response({
            'error': 'You are not following this user',
            'following': False
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_follow_status(request, user_id):
    """
    Check if current user is following another user
    """
    try:
        user_to_check = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    is_following = request.user.is_following(user_to_check)
    
    return Response({
        'is_following': is_following,
        'user_id': user_id,
        'username': user_to_check.username
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_followers(request):
    """
    Get list of users who follow the current user
    """
    followers = request.user.get_followers()
    serializer = UserSerializer(followers, many=True)
    return Response({
        'count': len(serializer.data),
        'followers': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_following(request):
    """
    Get list of users the current user is following
    """
    following = request.user.get_following()
    serializer = UserSerializer(following, many=True)
    return Response({
        'count': len(serializer.data),
        'following': serializer.data
    })