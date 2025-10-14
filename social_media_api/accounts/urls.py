from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    
    # User profiles
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    
    # User details
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    # Follow/unfollow
    path('users/<int:user_id>/follow/', views.follow_user, name='follow-user'),
    path('users/<int:user_id>/unfollow/', views.unfollow_user, name='unfollow-user'),
]