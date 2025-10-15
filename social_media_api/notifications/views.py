from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer

class NotificationListView(generics.ListAPIView):
    """View to list all notifications for the current user"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class UnreadNotificationListView(generics.ListAPIView):
    """View to list unread notifications for the current user"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, read=False)

class NotificationMarkAsReadView(generics.GenericAPIView):
    """View to mark a notification as read"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationUpdateSerializer
    
    def post(self, request, notification_id):
        notification = generics.get_object_or_404(
            Notification, 
            id=notification_id, 
            recipient=request.user
        )
        notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

class NotificationMarkAllAsReadView(generics.GenericAPIView):
    """View to mark all notifications as read"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        notifications = Notification.objects.filter(recipient=request.user, read=False)
        notifications.update(read=True)
        return Response(
            {"message": "All notifications marked as read."},
            status=status.HTTP_200_OK
        )

class NotificationCountView(generics.GenericAPIView):
    """View to get count of unread notifications"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        count = Notification.objects.filter(recipient=request.user, read=False).count()
        return Response({"unread_count": count})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_follow_notification(follower, followed):
    """Helper function to create follow notification"""
    if follower != followed:
        Notification.objects.create(
            recipient=followed,
            actor=follower,
            verb='started following you'
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_comment_notification(comment_author, post_author, post, comment):
    """Helper function to create comment notification"""
    if comment_author != post_author:
        Notification.objects.create(
            recipient=post_author,
            actor=comment_author,
            verb='commented on your post',
            target=post
        )

