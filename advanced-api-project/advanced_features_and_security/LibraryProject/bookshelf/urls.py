from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('my-books/', views.my_books, name='my_books'),
    path('search/', views.search_books, name='search_books'),
    path('form-examples/', views.form_examples, name='form_examples'),
    path('form-examples/', views.form_examples, name='form_examples'),
    path('example-form/', views.example_form_view, name='example_form'),
    path('form-success/', views.form_success, name='form_success'),
]