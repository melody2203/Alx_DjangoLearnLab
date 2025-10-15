from .models import Notification

def create_follow_notification(follower, followed):
    """Create notification when someone follows a user"""
    if follower != followed:
        Notification.objects.create(
            recipient=followed,
            actor=follower,
            verb='started following you'
        )

def create_comment_notification(comment_author, post_author, post, comment):
    """Create notification when someone comments on a post"""
    if comment_author != post_author:
        Notification.objects.create(
            recipient=post_author,
            actor=comment_author,
            verb='commented on your post',
            target=post
        )

def create_like_notification(liker, post_author, post):
    """Create notification when someone likes a post"""
    if liker != post_author:
        Notification.objects.create(
            recipient=post_author,
            actor=liker,
            verb='liked your post',
            target=post
        )