from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Show these fields in the list view
    list_display = ("title", "author", "publication_year")
    
    # Add filters in the sidebar
    list_filter = ("publication_year", "author")
    
    # Add a search box (searchable by title and author)
    search_fields = ("title", "author")
