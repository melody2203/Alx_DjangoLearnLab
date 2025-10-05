from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.urls import path
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path('books/', include('bookshelf.urls')),  # Include bookshelf app URLs
    path('', RedirectView.as_view(url='/books/', permanent=True)),  # Redirect root to books
    path('', lambda request: redirect('admin/')),
    path("", include("relationship_app.urls")),
    path("roles/", include('relationship_app.urls')),
]
