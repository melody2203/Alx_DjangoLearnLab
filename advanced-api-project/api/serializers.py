# api/serializers.py
from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer serializes all fields of the Book model.
    
    Includes custom validation to ensure publication_year is not in the future.
    Handles the serialization of book data including title, publication year, and author.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation method to ensure publication_year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer serializes Author model with nested book information.
    
    Fields:
    - name: The author's name
    - books: Nested BookSerializer that dynamically serializes all related books
             This demonstrates handling of nested relationships in DRF serializers
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']