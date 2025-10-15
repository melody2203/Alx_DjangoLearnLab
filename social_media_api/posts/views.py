from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.filters import SearchFilter
from accounts import models
from .models import Post, Comment
from .serializers import (
    PostSerializer, PostCreateSerializer, 
    CommentSerializer, CommentCreateSerializer
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['author']
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author']
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
class PostViewSet(viewsets.ModelViewSet):
    # ... existing code ...
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        """
        Get feed of posts from users that the current user follows
        """
        # Get users that the current user follows
        following_users = request.user.following.all()
        
        # Get posts from followed users, ordered by most recent
        feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Paginate the results
        page = self.paginate_queryset(feed_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(feed_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def explore(self, request):
        """
        Get popular posts from all users (for discovery)
        """
        # Get posts with most comments, ordered by comment count and recency
        explore_posts = Post.objects.annotate(
            comments_count=models.Count('comments')
        ).order_by('-comments_count', '-created_at')
        
        # Paginate the results
        page = self.paginate_queryset(explore_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(explore_posts, many=True)
        return Response(serializer.data)
