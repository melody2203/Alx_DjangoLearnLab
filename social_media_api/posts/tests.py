from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Post, Comment

class PostTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.client = APIClient()
        
    def test_create_post(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/posts/', {
            'title': 'Test Post',
            'content': 'This is a test post content'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')
    
    def test_update_own_post(self):
        post = Post.objects.create(author=self.user1, title='Original Title', content='Content')
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(f'/api/posts/{post.id}/', {
            'title': 'Updated Title'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Title')
    
    def test_cannot_update_others_post(self):
        post = Post.objects.create(author=self.user1, title='Original Title', content='Content')
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(f'/api/posts/{post.id}/', {
            'title': 'Hacked Title'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CommentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(author=self.user, title='Test Post', content='Content')
        self.client = APIClient()
        
    def test_create_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/comments/', {
            'post': self.post.id,
            'content': 'This is a test comment'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, 'This is a test comment')
