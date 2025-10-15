import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post, Comment

User = get_user_model()

def create_test_posts():
    print("Creating test posts and comments...")
    
    # Get or create test users
    user1, created = User.objects.get_or_create(
        username='alice',
        defaults={'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Smith'}
    )
    if created:
        user1.set_password('testpass123')
        user1.save()
    
    user2, created = User.objects.get_or_create(
        username='bob',
        defaults={'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Johnson'}
    )
    if created:
        user2.set_password('testpass123')
        user2.save()
    
    # Create test posts
    posts_data = [
        {
            'author': user1,
            'title': 'Welcome to our Social Network!',
            'content': 'This is our first post. Feel free to share your thoughts and connect with others!'
        },
        {
            'author': user2,
            'title': 'The Future of Technology',
            'content': 'I believe AI and machine learning will revolutionize how we interact with technology in the coming years.'
        },
        {
            'author': user1,
            'title': 'My Travel Adventures',
            'content': 'Just returned from an amazing trip to Japan. The culture, food, and people were incredible!'
        },
        {
            'author': user2,
            'title': 'Book Recommendations',
            'content': 'Recently finished "The Three-Body Problem" - highly recommended for sci-fi fans!'
        }
    ]
    
    for post_data in posts_data:
        post, created = Post.objects.get_or_create(
            title=post_data['title'],
            defaults=post_data
        )
        if created:
            print(f"✅ Created post: {post.title}")
            
            # Create some comments
            comments_data = [
                {'author': user2, 'content': 'Great post! Looking forward to more content.'},
                {'author': user1, 'content': 'Thanks for sharing your thoughts!'},
            ]
            
            for comment_data in comments_data:
                Comment.objects.create(
                    post=post,
                    author=comment_data['author'],
                    content=comment_data['content']
                )
                print(f"✅ Created comment on: {post.title}")
    
    print("\n🎉 Test data creation completed!")
    print(f"📊 Summary:")
    print(f"   - Posts: {Post.objects.count()}")
    print(f"   - Comments: {Comment.objects.count()}")

if __name__ == '__main__':
    create_test_posts()