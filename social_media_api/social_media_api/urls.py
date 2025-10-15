from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Use accounts instead of authentication
    path('api/', include('posts.urls')),
    path('api/notifications/', include('notifications.urls')),
]
