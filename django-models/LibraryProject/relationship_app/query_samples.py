import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# ---- Sample Queries ---- #

# 1. Query all books by a specific author
author = Author.objects.get(name="J.K. Rowling")
books_by_author = author.books.all()
print("Books by J.K. Rowling:", [book.title for book in books_by_author])

# 2. List all books in a library
library = Library.objects.get(name="Central Library")
books_in_library = library.books.all()
print("Books in Central Library:", [book.title for book in books_in_library])

# 3. Retrieve the librarian for a library
library = Library.objects.get(name="Central Library")
librarian = library.librarian  # OneToOne relation
print(f"Librarian of {library.name}:", librarian.name)
