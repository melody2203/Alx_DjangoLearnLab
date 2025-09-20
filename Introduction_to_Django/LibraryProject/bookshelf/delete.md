4. Delete
# Command:
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Expected Output: (1, {'bookshelf.Book': 1})
Confirm deletion: Book.objects.all()
Expected Output: <QuerySet []>