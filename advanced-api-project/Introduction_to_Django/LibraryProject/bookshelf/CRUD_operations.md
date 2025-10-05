CRUD Operations with Django Shell
1. Create
# Command:
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
Expected Output: <Book: 1984 by George Orwell (1949)>
2. Retrieve
# Command:
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.id, book.title, book.author, book.publication_year
Expected Output: (1, '1984', 'George Orwell', 1949)
Alternative (list all books):
Book.objects.all()
Expected Output: <QuerySet [<Book: 1984 by George Orwell (1949)>]>
3. Update
# Command:
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
Expected Output: <Book: Nineteen Eighty-Four by George Orwell (1949)>
4. Delete
# Command:
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Expected Output: (1, {'bookshelf.Book': 1})
Confirm deletion: Book.objects.all()
Expected Output: <QuerySet []>