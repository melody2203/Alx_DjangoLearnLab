from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', lambda request: redirect('admin/')),
    path("", include("relationship_app.urls")),
    path("roles/", include('relationship_app.urls')),
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('my-books/', views.my_books, name='my_books'),
]
