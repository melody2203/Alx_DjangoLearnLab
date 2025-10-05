# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book')

urlpatterns = [
    # Authentication endpoints
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    
    # Public endpoint (no authentication required)
    path('books/', BookList.as_view(), name='book-list'),
    
    # Protected endpoints (require authentication)
    path('', include(router.urls)),
]