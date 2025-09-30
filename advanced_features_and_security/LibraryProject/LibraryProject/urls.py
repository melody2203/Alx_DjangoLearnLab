from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', lambda request: redirect('admin/')),
    # path("", include("relationship_app.urls")),
    path("roles/", include('relationship_app.urls')),
]
