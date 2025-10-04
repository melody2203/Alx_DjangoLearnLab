# api/views.py
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    Provides the following actions:
    - list: GET /books_all/
    - create: POST /books_all/
    - retrieve: GET /books_all/{id}/
    - update: PUT /books_all/{id}/
    - partial_update: PATCH /books_all/{id}/
    - destroy: DELETE /books_all/{id}/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer