from django.urls import path
from .views import list_books, LibraryDetailView   # ✅ explicit imports

urlpatterns = [
    path("books/", list_books, name="list_books"),   # ✅ contains path + list_books
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),  # ✅ LibraryDetailView
]

