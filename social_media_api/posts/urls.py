from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.FeedView.as_view(), name='feed'),
    # Like/Unlike URLs with exact patterns required
    path('posts/<int:pk>/like/', views.LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', views.UnlikePostView.as_view(), name='unlike-post'),
]