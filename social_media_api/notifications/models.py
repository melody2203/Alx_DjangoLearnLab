from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actor_notifications'
    )
    
    verb = models.CharField(max_length=255)
    
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['recipient', 'read']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.actor.username} {self.verb} - {self.recipient.username}"
    
    def mark_as_read(self):
        self.read = True
        self.save()
    
    def mark_as_unread(self):
        self.read = False
        self.save()
