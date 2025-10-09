from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create authors
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
