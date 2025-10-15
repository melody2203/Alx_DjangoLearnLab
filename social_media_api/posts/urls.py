from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    # Add the feed endpoint
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('posts/<int:post_id>/like/', views.LikePostView.as_view(), name='like-post'),
    path('posts/<int:post_id>/unlike/', views.UnlikePostView.as_view(), name='unlike-post'),
]