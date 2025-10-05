from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    print("=== ADMIN VIEW ACCESSED ===")
    print(f"User: {request.user.username}")
    print(f"Role: {request.user.userprofile.role}")
    return render(request, 'relationship_app/admin_view.html')
