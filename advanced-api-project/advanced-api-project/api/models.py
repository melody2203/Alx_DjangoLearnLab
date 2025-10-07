"""
Models for the API application.

This module defines the data models for Author and Book entities,
establishing a one-to-many relationship where one Author can have multiple Books.
"""

from django.db import models


class Author(models.Model):
    """
    Author model representing a book author.
    
    Attributes:
        name (CharField): The name of the author, stored as a string with maximum length of 100 characters.
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """String representation of the Author model."""
        return self.name
    
    class Meta:
        """Meta options for the Author model."""
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    """
    Book model representing a published book.
    
    Attributes:
        title (CharField): The title of the book, stored as a string with maximum length of 200 characters.
        publication_year (IntegerField): The year the book was published.
        author (ForeignKey): A foreign key relationship to the Author model, establishing that one author can have multiple books.
                            When an author is deleted, all their books will also be deleted (CASCADE).
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,  # If author is deleted, all their books are also deleted
        related_name='books'  # Enables reverse relation: author.books.all()
    )
    
    def __str__(self):
        """String representation of the Book model."""
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        """Meta options for the Book model."""
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-publication_year']  # Default ordering by publication year (newest first)
