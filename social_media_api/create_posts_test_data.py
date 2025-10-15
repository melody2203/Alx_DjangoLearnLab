import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post, Comment

User = get_user_model()

def create_follow_test_data():
    print("Creating follow relationships and feed test data...")
    
    # Create test users
    users_data = [
        {'username': 'alice', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Smith'},
        {'username': 'bob', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Johnson'},
        {'username': 'charlie', 'email': 'charlie@example.com', 'first_name': 'Charlie', 'last_name': 'Brown'},
        {'username': 'diana', 'email': 'diana@example.com', 'first_name': 'Diana', 'last_name': 'Prince'},
    ]
    
    users = {}
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print(f"✅ Created user: {user.username}")
        users[user.username] = user
    
    # Create follow relationships
    follow_relationships = [
        ('alice', 'bob'),
        ('alice', 'charlie'),
        ('bob', 'alice'),
        ('bob', 'diana'),
        ('charlie', 'alice'),
        ('diana', 'alice'),
        ('diana', 'bob'),
    ]
    
    for follower, followed in follow_relationships:
        if users[follower].follow(users[followed]):
            print(f"✅ {follower} is now following {followed}")
    
    # Create posts from different users
    posts_data = [
        {
            'author': users['alice'],
            'title': 'Alice: My Morning Routine',
            'content': 'Started my day with meditation and a healthy breakfast. Feeling great!'
        },
        {
            'author': users['bob'],
            'title': 'Bob: Tech News',
            'content': 'Just read about the latest AI developments. The future is exciting!'
        },
        {
            'author': users['charlie'],
            'title': 'Charlie: Book Review',
            'content': 'Finished reading "Dune" - an amazing sci-fi masterpiece!'
        },
        {
            'author': users['diana'],
            'title': 'Diana: Travel Plans',
            'content': 'Planning my next trip to Italy. Any recommendations?'
        },
        {
            'author': users['alice'],
            'title': 'Alice: Work Update',
            'content': 'Just completed a major project at work. Time to celebrate!'
        },
        {
            'author': users['bob'],
            'title': 'Bob: Programming Tips',
            'content': 'Here are my top 5 Python tips for beginners...'
        },
    ]
    
    for post_data in posts_data:
        post, created = Post.objects.get_or_create(
            title=post_data['title'],
            defaults=post_data
        )
        if created:
            print(f"✅ Created post: {post.title}")
            
            # Create some comments
            comment_authors = [users['bob'], users['charlie'], users['diana']]
            for comment_author in comment_authors:
                if comment_author != post.author:  # Don't comment on own posts
                    Comment.objects.create(
                        post=post,
                        author=comment_author,
                        content=f'Great post, {post.author.first_name}!'
                    )
    
    print("\n🎉 Follow test data creation completed!")
    print(f"📊 Summary:")
    print(f"   - Users: {User.objects.count()}")
    print(f"   - Posts: {Post.objects.count()}")
    print(f"   - Comments: {Comment.objects.count()}")
    print(f"   - Follow relationships: {sum(user.following_count for user in User.objects.all())}")
    
    # Show follow relationships
    print("\n🤝 Follow Relationships:")
    for user in User.objects.all():
        following = [u.username for u in user.get_following()]
        followers = [u.username for u in user.get_followers()]
        print(f"   {user.username}:")
        print(f"     Following: {following}")
        print(f"     Followers: {followers}")

if __name__ == '__main__':
    create_follow_test_data()