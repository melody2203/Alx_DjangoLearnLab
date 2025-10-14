from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'followers_count']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['followers_count', 'following_count']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {
            'fields': ('bio', 'profile_picture', 'followers')
        }),
    )
