from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import BookForm, BookSearchForm, UserRegistrationForm, ContactForm
from .forms import ExampleForm, BookForm, BookSearchForm

def example_form_view(request):
    """
    View to demonstrate the ExampleForm with security features
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the secure, validated data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            # ... process other fields
            
            # In a real application, you would save to database here
            messages.success(request, f'Thank you {name}! Your information has been securely processed.')
            return redirect('bookshelf:form_success')
    else:
        form = ExampleForm()
    
    # Also include other forms for the template
    book_form = BookForm()
    search_form = BookSearchForm()
    
    context = {
        'example_form': form,
        'book_form': book_form,
        'search_form': search_form,
    }
    
    return render(request, 'bookshelf/form_example.html', context)

def form_success(request):
    """Success page after form submission"""
    return render(request, 'bookshelf/form_success.html')
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
