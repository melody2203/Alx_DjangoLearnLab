# api/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
import json

class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints including CRUD operations,
    filtering, searching, ordering, and authentication.
    """
    
    def setUp(self):
        """
        Set up test data and client for all test cases.
        Configure separate test database and create test users and data.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword123',
            email='admin@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        self.author3 = Author.objects.create(name='J.R.R. Tolkien')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author3
        )
        self.book4 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        
        # Initialize API client
        self.client = APIClient()
        
        # URLs for testing
        self.book_list_url = reverse('book-list')
        self.book_create_url = reverse('book-create')
        self.author_list_url = reverse('author-list')

    # ===== AUTHENTICATION & PERMISSION TESTS =====
    
    def test_unauthenticated_access_to_book_list(self):
        """
        Test that unauthenticated users can access book list (read-only).
        Expected: 200 OK
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Should return all 4 books
    
    def test_unauthenticated_access_to_book_detail(self):
        """
        Test that unauthenticated users can access book details (read-only).
        Expected: 200 OK
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_unauthenticated_user_cannot_create_book(self):
        """
        Test that unauthenticated users cannot create books.
        Expected: 403 Forbidden or 401 Unauthorized
        """
        book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(self.book_create_url, book_data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_authenticated_user_can_create_book(self):
        """
        Test that authenticated users can create books.
        Expected: 201 Created
        """
        self.client.force_authenticate(user=self.user)
        book_data = {
            'title': 'Authenticated User Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.post(self.book_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['title'], 'Authenticated User Book')
        self.assertEqual(Book.objects.count(), 5)  # Should have one more book

    # ===== CRUD OPERATION TESTS =====
    
    def test_create_book_with_valid_data(self):
        """
        Test creating a book with valid data returns 201 and correct data.
        """
        self.client.force_authenticate(user=self.user)
        book_data = {
            'title': 'Test Book Creation',
            'publication_year': 2023,
            'author': self.author2.pk
        }
        response = self.client.post(self.book_create_url, book_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Book created successfully')
        self.assertEqual(response.data['data']['title'], 'Test Book Creation')
        self.assertEqual(response.data['data']['publication_year'], 2023)
    
    def test_create_book_with_future_publication_year(self):
        """
        Test that creating a book with future publication year fails validation.
        Expected: 400 Bad Request
        """
        self.client.force_authenticate(user=self.user)
        book_data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.pk
        }
        response = self.client.post(self.book_create_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_retrieve_book_detail(self):
        """
        Test retrieving a single book by ID returns correct data.
        """
        url = reverse('book-detail', kwargs={'pk': self.book2.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '1984')
        self.assertEqual(response.data['publication_year'], 1949)
        self.assertEqual(response.data['author'], self.author2.pk)
    
    def test_update_book(self):
        """
        Test updating an existing book with valid data.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        update_data = {
            'title': 'Updated Harry Potter Title',
            'publication_year': 1997,
            'author': self.author1.pk
        }
        response = self.client.put(url, update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Book updated successfully')
        self.assertEqual(response.data['data']['title'], 'Updated Harry Potter Title')
        
        # Verify the update in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Harry Potter Title')
    
    def test_delete_book(self):
        """
        Test deleting a book removes it from database.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete', kwargs={'pk': self.book3.pk})
        
        initial_count = Book.objects.count()
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
        
        # Verify book no longer exists
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book3.pk)

    # ===== FILTERING TESTS =====
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        url = f"{self.book_list_url}?publication_year=1997"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author ID.
        """
        url = f"{self.book_list_url}?author={self.author1.pk}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # J.K. Rowling has 2 books
        titles = [book['title'] for book in response.data]
        self.assertIn('Harry Potter and the Philosopher\'s Stone', titles)
        self.assertIn('Harry Potter and the Chamber of Secrets', titles)
    
    def test_filter_books_by_author_name(self):
        """
        Test filtering books by author name.
        """
        url = f"{self.book_list_url}?author__name=J.K. Rowling"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ===== SEARCHING TESTS =====
    
    def test_search_books_by_title(self):
        """
        Test searching books by title using search parameter.
        """
        url = f"{self.book_list_url}?search=Harry"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
        titles = [book['title'] for book in response.data]
        self.assertIn('Harry Potter and the Philosopher\'s Stone', titles)
        self.assertIn('Harry Potter and the Chamber of Secrets', titles)
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name using search parameter.
        """
        url = f"{self.book_list_url}?search=Orwell"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    # ===== ORDERING TESTS =====
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        """
        url = f"{self.book_list_url}?ordering=title"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))  # Should be in alphabetical order
    
    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        """
        url = f"{self.book_list_url}?ordering=-publication_year"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        publication_years = [book['publication_year'] for book in response.data]
        self.assertEqual(publication_years, sorted(publication_years, reverse=True))
    
    def test_order_books_by_author_name(self):
        """
        Test ordering books by author name.
        """
        url = f"{self.book_list_url}?ordering=author__name"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be ordered by author name alphabetically

    # ===== COMBINED QUERY TESTS =====
    
    def test_combined_filter_search_order(self):
        """
        Test combined filtering, searching, and ordering in single query.
        """
        url = f"{self.book_list_url}?author__name=J.K. Rowling&search=Harry&ordering=-publication_year"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Should be ordered by publication year descending
        self.assertEqual(response.data[0]['publication_year'], 1998)
        self.assertEqual(response.data[1]['publication_year'], 1997)

    # ===== AUTHOR API TESTS =====
    
    def test_author_list_with_books(self):
        """
        Test that author list returns authors with nested books.
        """
        response = self.client.get(self.author_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Check that J.K. Rowling has 2 books
        rowling_data = next(author for author in response.data if author['name'] == 'J.K. Rowling')
        self.assertEqual(len(rowling_data['books']), 2)
    
    def test_author_detail_with_books(self):
        """
        Test that author detail returns author with nested books.
        """
        url = reverse('author-detail', kwargs={'pk': self.author1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'J.K. Rowling')
        self.assertEqual(len(response.data['books']), 2)

    # ===== ERROR HANDLING TESTS =====
    
    def test_retrieve_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist returns 404.
        """
        url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_nonexistent_book(self):
        """
        Test updating a book that doesn't exist returns 404.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': 9999})
        update_data = {
            'title': 'Nonexistent Book',
            'publication_year': 2023,
            'author': self.author1.pk
        }
        response = self.client.put(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ModelTestCase(TestCase):
    """
    Test cases for models to ensure they work correctly.
    """
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2023,
            author=self.author
        )
    
    def test_author_creation(self):
        """Test Author model creation and string representation."""
        self.assertEqual(str(self.author), 'Test Author')
        self.assertEqual(Author.objects.count(), 1)
    
    def test_book_creation(self):
        """Test Book model creation and string representation."""
        self.assertEqual(str(self.book), 'Test Book by Test Author')
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(self.book.author.name, 'Test Author')
    
    def test_author_book_relationship(self):
        """Test the one-to-many relationship between Author and Book."""
        # Create another book by the same author
        Book.objects.create(
            title='Another Test Book',
            publication_year=2024,
            author=self.author
        )
        
        self.assertEqual(self.author.books.count(), 2)
        self.assertEqual(Book.objects.count(), 2)