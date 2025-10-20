from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    
    # User Profile URLs
    path('profile/', views.CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('users/<int:user_id>/profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # Follow/Unfollow URLs - Using the exact patterns required
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow-user'),
    
    # Followers/Following URLs
    path('users/<int:user_id>/followers/', views.UserFollowersView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', views.UserFollowingView.as_view(), name='user-following'),
    
    # Additional URL to show all users
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('token/', views.CustomAuthToken.as_view(), name='api-token'),
]