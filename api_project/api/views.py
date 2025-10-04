# api/views.py
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Book
from .serializers import BookSerializer

# Public view - anyone can see the book list
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

# Protected ViewSet - requires authentication for write operations
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Anyone can view books
            permission_classes = [AllowAny]
        else:
            # Only authenticated users can create, update, delete
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]