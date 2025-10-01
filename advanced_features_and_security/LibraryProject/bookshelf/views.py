from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Book, CustomUser
from .forms import BookForm

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View to list all books - requires can_view permission"""
    books = Book.objects.all()
    
    # Filter based on user permissions and ownership
    if not request.user.has_perm('bookshelf.can_view_all'):
        # Users can see public books and their own books
        books = books.filter(
            Q(is_public=True) | Q(added_by=request.user)
        )
    
    context = {
        'books': books,
        'can_create': request.user.has_perm('bookshelf.can_create')
    }
    return render(request, 'bookshelf/book_list.html', context)

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """View to create new book - requires can_create permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Create'})

@login_required
def book_edit(request, pk):
    """View to edit book - requires can_edit permission and object-level permission"""
    book = get_object_or_404(Book, pk=pk)
    
    # Check both model-level and object-level permissions
    if not (request.user.has_perm('bookshelf.can_edit') and 
            book.has_edit_permission(request.user)):
        return HttpResponseForbidden("You don't have permission to edit this book.")
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Edit'})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """View to delete book - requires can_delete permission"""
    book = get_object_or_404(Book, pk=pk)
    
    # Additional object-level permission check
    if not book.has_delete_permission(request.user):
        return HttpResponseForbidden("You don't have permission to delete this book.")
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

@login_required
def my_books(request):
    """View to show user's own books"""
    books = Book.objects.filter(added_by=request.user)
    return render(request, 'bookshelf/my_books.html', {'books': books})
