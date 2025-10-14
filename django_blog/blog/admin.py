from django.contrib import admin
from .models import Post, Profile, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'date_updated')
    list_filter = ('date_posted', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'date_posted'
    ordering = ('-date_posted',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    search_fields = ('user__username', 'bio', 'location')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)