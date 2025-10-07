"""
Serializers for the API application.

This module defines custom serializers for the Author and Book models using Django REST Framework.
These serializers handle complex data structures, nested relationships, and custom validation.
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles serialization and deserialization of Book instances,
    including custom validation for the publication_year field.
    
    Fields:
        id (IntegerField): The primary key of the book (read-only)
        title (CharField): The title of the book
        publication_year (IntegerField): The year the book was published
        author (PrimaryKeyRelatedField): The ID of the author (for write operations)
    
    Validation:
        - Custom validation ensures publication_year is not in the future
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']
    
    def validate_publication_year(self, value):
        """
        Validate that the publication year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested book relationships.
    
    This serializer handles serialization of Author instances including their related books
    through a nested BookSerializer. The books field is read-only and dynamically includes
    all books written by the author.
    
    Fields:
        id (IntegerField): The primary key of the author (read-only)
        name (CharField): The name of the author
        books (BookSerializer): Nested serializer for all books by this author (read-only)
    
    The nested relationship demonstrates how to handle complex data structures in DRF,
    allowing clients to receive author data along with their complete book information
    in a single API response.
    """
    
    # Nested serializer for related books
    # Using BookSerializer to include complete book information
    # read_only=True ensures this field is only used for serialization (output)
    # many=True indicates this is a one-to-many relationship
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id']