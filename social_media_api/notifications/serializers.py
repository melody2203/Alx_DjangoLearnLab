from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    target_object = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_username', 'actor', 'actor_username',
            'verb', 'target', 'target_object', 'timestamp', 'read'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def get_target_object(self, obj):
        """Serialize the target object based on its content type"""
        if obj.target:
            # You can customize this based on your model serializers
            if hasattr(obj.target, 'title'):  # Post
                return {
                    'type': 'post',
                    'id': obj.target.id,
                    'title': obj.target.title
                }
            elif hasattr(obj.target, 'content'):  # Comment
                return {
                    'type': 'comment',
                    'id': obj.target.id,
                    'content': obj.target.content[:50]  # Preview
                }
        return None

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['read']