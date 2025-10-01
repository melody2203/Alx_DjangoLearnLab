# from django import forms
# from .models import Book

# class BookForm(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ['title', 'author', 'publication_year', 'is_public']
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter book title'
#             }),
#             'author': forms.TextInput(attrs={
#                 'class': 'form-control', 
#                 'placeholder': 'Enter author name'
#             }),
#             'publication_year': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter publication year',
#                 'min': 1000,
#                 'max': 2030
#             }),
#             'is_public': forms.CheckboxInput(attrs={
#                 'class': 'form-check-input'
#             }),
#         }
#         labels = {
#             'is_public': 'Make this book visible to all users'
#         }

#     def clean_publication_year(self):
#         """Additional validation for publication year"""
#         publication_year = self.cleaned_data.get('publication_year')
#         if publication_year < 1000 or publication_year > 2030:
#             raise forms.ValidationError("Please enter a valid publication year (1000-2030)")
#         return publication_year

#     def clean_title(self):
#         """Sanitize title input"""
#         title = self.cleaned_data.get('title')
#         if title:
#             # Basic sanitization - remove any HTML tags
#             import html
#             title = html.escape(title.strip())
#         return title

#     def clean_author(self):
#         """Sanitize author input"""
#         author = self.cleaned_data.get('author')
#         if author:
#             # Basic sanitization - remove any HTML tags
#             import html
#             author = html.escape(author.strip())
#         return author