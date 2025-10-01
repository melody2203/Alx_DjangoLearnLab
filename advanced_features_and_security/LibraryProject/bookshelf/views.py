from django.shortcuts import render
from django.http import HttpResponse

# Minimal placeholder views - just to get migrations working
def book_list(request):
    return HttpResponse("Book list - working")

def book_create(request):
    return HttpResponse("Create book - working")

def book_edit(request, pk):
    return HttpResponse(f"Edit book {pk} - working")

def book_delete(request, pk):
    return HttpResponse(f"Delete book {pk} - working")

def my_books(request):
    return HttpResponse("My books - working")

def search_books(request):
    return HttpResponse("Search books - working")
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required, permission_required
# from django.contrib import messages
# from django.http import HttpResponseForbidden, HttpResponseBadRequest
# from django.db.models import Q
# from django.core.exceptions import ValidationError
# import bleach  # For HTML sanitization
# from .models import Book, CustomUser
# from .forms import BookForm

# # Safe list of allowed HTML tags for sanitization
# ALLOWED_HTML_TAGS = ['b', 'i', 'em', 'strong', 'p', 'br']

# @login_required
# @permission_required('bookshelf.can_view', raise_exception=True)
# def book_list(request):
#     """
#     Secure book list view with proper input validation and SQL injection prevention.
#     Uses Django ORM to safely handle database queries.
#     """
#     # Safely get search parameter using GET method
#     search_query = request.GET.get('q', '').strip()
    
#     # Start with base queryset using safe ORM methods
#     books = Book.objects.all()
    
#     # Apply filters based on user permissions using safe ORM methods
#     if not request.user.has_perm('bookshelf.can_view_all'):
#         books = books.filter(
#             Q(is_public=True) | Q(added_by=request.user)
#         )
    
#     # Safe search implementation using parameterized ORM queries
#     if search_query:
#         # Sanitize search query to prevent XSS and injection
#         sanitized_query = bleach.clean(
#             search_query, 
#             tags=[], 
#             strip=True
#         )
        
#         # Use Django ORM to safely search - prevents SQL injection
#         books = books.filter(
#             Q(title__icontains=sanitized_query) |
#             Q(author__icontains=sanitized_query)
#         )
    
#     # Safe ordering using validated field names
#     sort_by = request.GET.get('sort', 'title')
#     if sort_by in ['title', 'author', 'publication_year', 'created_at']:
#         books = books.order_by(sort_by)
#     else:
#         # Default safe ordering
#         books = books.order_by('title')
    
#     context = {
#         'books': books,
#         'can_create': request.user.has_perm('bookshelf.can_create'),
#         'search_query': search_query,
#     }
#     return render(request, 'bookshelf/book_list.html', context)

# @login_required
# @permission_required('bookshelf.can_create', raise_exception=True)
# def book_create(request):
#     """
#     Secure book creation view with form validation and input sanitization.
#     """
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             try:
#                 # Sanitize user input before saving
#                 book = form.save(commit=False)
#                 book.added_by = request.user
                
#                 # Additional manual validation
#                 if book.publication_year < 1000 or book.publication_year > 2030:
#                     raise ValidationError("Invalid publication year")
                
#                 book.save()
#                 messages.success(request, 'Book added successfully!')
#                 return redirect('book_list')
                
#             except ValidationError as e:
#                 messages.error(request, f'Validation error: {e}')
#             except Exception as e:
#                 # Log security events
#                 import logging
#                 logger = logging.getLogger('django.security')
#                 logger.warning(f'Book creation error: {e}')
#                 messages.error(request, 'An error occurred while creating the book.')
#     else:
#         form = BookForm()
    
#     return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Create'})

# @login_required
# def book_edit(request, pk):
#     """
#     Secure book editing with proper permission checks and input validation.
#     """
#     # Safe object retrieval with proper error handling
#     book = get_object_or_404(Book, pk=pk)
    
#     # Check both model-level and object-level permissions
#     if not (request.user.has_perm('bookshelf.can_edit') and 
#             book.has_edit_permission(request.user)):
#         return HttpResponseForbidden("You don't have permission to edit this book.")
    
#     if request.method == 'POST':
#         form = BookForm(request.POST, instance=book)
#         if form.is_valid():
#             try:
#                 # Additional security validation
#                 book = form.save(commit=False)
                
#                 # Validate publication year
#                 if book.publication_year < 1000 or book.publication_year > 2030:
#                     raise ValidationError("Invalid publication year")
                
#                 form.save()
#                 messages.success(request, 'Book updated successfully!')
#                 return redirect('book_list')
                
#             except ValidationError as e:
#                 messages.error(request, f'Validation error: {e}')
#             except Exception as e:
#                 # Log security events
#                 import logging
#                 logger = logging.getLogger('django.security')
#                 logger.warning(f'Book edit error: {e}')
#                 messages.error(request, 'An error occurred while updating the book.')
#     else:
#         form = BookForm(instance=book)
    
#     return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Edit'})

# @login_required
# @permission_required('bookshelf.can_delete', raise_exception=True)
# def book_delete(request, pk):
#     """
#     Secure book deletion with CSRF protection and permission validation.
#     """
#     # Only allow POST method for deletion (prevents CSRF via GET)
#     if request.method != 'POST':
#         return HttpResponseBadRequest("Invalid method")
    
#     book = get_object_or_404(Book, pk=pk)
    
#     # Additional object-level permission check
#     if not book.has_delete_permission(request.user):
#         return HttpResponseForbidden("You don't have permission to delete this book.")
    
#     try:
#         book_title = str(book.title)  # Safe string conversion
#         book.delete()
#         messages.success(request, f'Book "{book_title}" deleted successfully!')
#     except Exception as e:
#         # Log security events
#         import logging
#         logger = logging.getLogger('django.security')
#         logger.error(f'Book deletion error: {e}')
#         messages.error(request, 'An error occurred while deleting the book.')
    
#     return redirect('book_list')

# @login_required
# def search_books(request):
#     """
#     Secure search functionality with input validation and sanitization.
#     """
#     if request.method != 'GET':
#         return HttpResponseBadRequest("Only GET method allowed for search")
    
#     query = request.GET.get('q', '').strip()
    
#     # Validate query length to prevent DoS attacks
#     if len(query) > 100:
#         messages.error(request, 'Search query too long.')
#         return redirect('book_list')
    
#     # Sanitize the query to prevent XSS
#     sanitized_query = bleach.clean(query, tags=[], strip=True)
    
#     if not sanitized_query:
#         messages.info(request, 'Please enter a search term.')
#         return redirect('book_list')
    
#     # Use safe ORM queries for search
#     books = Book.objects.filter(
#         Q(title__icontains=sanitized_query) |
#         Q(author__icontains=sanitized_query)
#     ).filter(
#         Q(is_public=True) | Q(added_by=request.user)
#     )
    
#     context = {
#         'books': books,
#         'search_query': sanitized_query,
#         'results_count': books.count(),
#     }
    
#     return render(request, 'bookshelf/search_results.html', context)
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required, permission_required
# from django.contrib import messages
# from django.http import HttpResponseForbidden
# from django.db.models import Q
# from .models import Book, CustomUser
# from .forms import BookForm

# @login_required
# @permission_required('bookshelf.can_view', raise_exception=True)
# def book_list(request):
#     """View to list all books - requires can_view permission"""
#     books = Book.objects.all()
    
#     # Filter based on user permissions and ownership
#     if not request.user.has_perm('bookshelf.can_view_all'):
#         # Users can see public books and their own books
#         books = books.filter(
#             Q(is_public=True) | Q(added_by=request.user)
#         )
    
#     context = {
#         'books': books,
#         'can_create': request.user.has_perm('bookshelf.can_create')
#     }
#     return render(request, 'bookshelf/book_list.html', context)

# @login_required
# @permission_required('bookshelf.can_create', raise_exception=True)
# def book_create(request):
#     """View to create new book - requires can_create permission"""
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             book = form.save(commit=False)
#             book.added_by = request.user
#             book.save()
#             messages.success(request, 'Book added successfully!')
#             return redirect('book_list')
#     else:
#         form = BookForm()
    
#     return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Create'})

# @login_required
# def book_edit(request, pk):
#     """View to edit book - requires can_edit permission and object-level permission"""
#     book = get_object_or_404(Book, pk=pk)
    
#     # Check both model-level and object-level permissions
#     if not (request.user.has_perm('bookshelf.can_edit') and 
#             book.has_edit_permission(request.user)):
#         return HttpResponseForbidden("You don't have permission to edit this book.")
    
#     if request.method == 'POST':
#         form = BookForm(request.POST, instance=book)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Book updated successfully!')
#             return redirect('book_list')
#     else:
#         form = BookForm(instance=book)
    
#     return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Edit'})

# @login_required
# @permission_required('bookshelf.can_delete', raise_exception=True)
# def book_delete(request, pk):
#     """View to delete book - requires can_delete permission"""
#     book = get_object_or_404(Book, pk=pk)
    
#     # Additional object-level permission check
#     if not book.has_delete_permission(request.user):
#         return HttpResponseForbidden("You don't have permission to delete this book.")
    
#     if request.method == 'POST':
#         book.delete()
#         messages.success(request, 'Book deleted successfully!')
#         return redirect('book_list')
    
#     return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# @login_required
# def my_books(request):
#     """View to show user's own books"""
#     books = Book.objects.filter(added_by=request.user)
#     return render(request, 'bookshelf/my_books.html', {'books': books})
