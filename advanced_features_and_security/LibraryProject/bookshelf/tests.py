from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from .models import Book

CustomUser = get_user_model()

class BookPermissionTests(TestCase):
    def setUp(self):
        # Create test users
        self.viewer_user = CustomUser.objects.create_user(
            email='viewer@example.com', 
            password='testpass123'
        )
        self.editor_user = CustomUser.objects.create_user(
            email='editor@example.com', 
            password='testpass123'
        )
        self.admin_user = CustomUser.objects.create_user(
            email='admin@example.com', 
            password='testpass123'
        )
        
        # Assign users to groups
        viewers_group = Group.objects.get(name='Viewers')
        editors_group = Group.objects.get(name='Editors')
        admins_group = Group.objects.get(name='Admins')
        
        self.viewer_user.groups.add(viewers_group)
        self.editor_user.groups.add(editors_group)
        self.admin_user.groups.add(admins_group)
        
        # Create test books
        self.public_book = Book.objects.create(
            title='Public Book',
            author='Test Author',
            publication_year=2020,
            added_by=self.admin_user,
            is_public=True
        )
        
        self.private_book = Book.objects.create(
            title='Private Book',
            author='Test Author',
            publication_year=2021,
            added_by=self.admin_user,
            is_public=False
        )

    def test_viewer_permissions(self):
        """Test that viewers can only view public books"""
        self.client.login(email='viewer@example.com', password='testpass123')
        
        # Can access book list
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        
        # Cannot create books
        response = self.client.get('/books/create/')
        self.assertEqual(response.status_code, 403)
        
        # Cannot edit books
        response = self.client.get(f'/books/{self.public_book.pk}/edit/')
        self.assertEqual(response.status_code, 403)

    def test_editor_permissions(self):
        """Test that editors can view, create, and edit books"""
        self.client.login(email='editor@example.com', password='testpass123')
        
        # Can access book list
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        
        # Can create books
        response = self.client.get('/books/create/')
        self.assertEqual(response.status_code, 200)
        
        # Can edit their own books
        own_book = Book.objects.create(
            title='Own Book',
            author='Editor',
            publication_year=2022,
            added_by=self.editor_user
        )
        response = self.client.get(f'/books/{own_book.pk}/edit/')
        self.assertEqual(response.status_code, 200)

    def test_admin_permissions(self):
        """Test that admins have all permissions"""
        self.client.login(email='admin@example.com', password='testpass123')
        
        # Can access book list
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        
        # Can create books
        response = self.client.get('/books/create/')
        self.assertEqual(response.status_code, 200)
        
        # Can delete books
        response = self.client.get(f'/books/{self.public_book.pk}/delete/')
        self.assertEqual(response.status_code, 200)

    def test_object_level_permissions(self):
        """Test object-level permission methods"""
        # Viewer should not have edit permission on admin's book
        self.assertFalse(self.public_book.has_edit_permission(self.viewer_user))
        
        # Admin should have edit permission on all books
        self.assertTrue(self.public_book.has_edit_permission(self.admin_user))
        
        # Owner should have edit permission on their own book
        own_book = Book.objects.create(
            title='Own Book',
            author='Editor',
            publication_year=2022,
            added_by=self.editor_user
        )
        self.assertTrue(own_book.has_edit_permission(self.editor_user))
