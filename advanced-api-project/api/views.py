# api/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books with advanced filtering, searching, and ordering capabilities.
    
    Filtering Features:
    - Filter by publication_year: /api/books/?publication_year=2020
    - Filter by author: /api/books/?author=1
    - Multiple filters: /api/books/?publication_year=2020&author=1
    
    Search Features:
    - Search in title and author name: /api/books/?search=django
    - Searches both book titles and author names
    
    Ordering Features:
    - Order by title: /api/books/?ordering=title
    - Order by publication_year: /api/books/?ordering=publication_year
    - Descending order: /api/books/?ordering=-publication_year
    
    Example combined query:
    /api/books/?publication_year=2020&search=python&ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filtering, searching, and ordering backends
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filtering configuration
    filterset_fields = ['publication_year', 'author', 'author__name']
    
    # Search configuration
    search_fields = ['title', 'author__name']
    
    # Ordering configuration
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    Provides read-only access to a specific Book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book with custom response handling.
    Handles POST requests to create new Book instances.
    Includes data validation from BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Custom method to handle book creation.
        Can be extended to add additional logic like logging, notifications, etc.
        """
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method to provide enhanced response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Book created successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    Handles PUT and PATCH requests to update Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        """
        Custom update method to provide enhanced response.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {
                'message': 'Book updated successfully',
                'data': serializer.data
            }
        )

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    Handles DELETE requests to remove Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class AuthorListView(generics.ListAPIView):
    """
    ListView for retrieving all authors with their nested books.
    Provides read-only access to all Author instances with their related books.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Add search and ordering for authors
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author by ID with nested books.
    Provides read-only access to a specific Author instance with related books.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
