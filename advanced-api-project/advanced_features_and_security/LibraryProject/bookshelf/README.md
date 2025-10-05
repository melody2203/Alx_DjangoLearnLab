# Bookshelf Permissions System

## Setup Instructions

1. **Run migrations** to create the Book model with custom permissions:
   ```bash
   python manage.py makemigrations bookshelf
   python manage.py migrate
2. Create default groups with assigned permissions:
   ```bash
    python manage.py setup_book_groups
3. Assign users to groups via Django Admin:
    - Go to /admin/auth/group/ to manage groups
    - Assign users to Viewers, Editors, or Admins groups
Groups and Permissions
Viewers
    Permissions: can_view
    Access: Can view public books and their own books
Editors
    Permissions: can_view, can_create, can_edit
    Access: Can view, create, and edit books (can edit their own books)
Admins
    Permissions: can_view, can_create, can_edit, can_delete
    Access: Full access to all book operation
Custom Permissions
The Book model defines these custom permissions:
    can_view: Permission to view books
    can_create: Permission to create new books
    can_edit: Permission to edit existing books
    can_delete: Permission to delete books

Testing
Run the test suite:
    ```bash
    python manage.py test bookshelf.tests.BookPermissionTests
Key Features
    Model-level permissions: Control access to book operations
    Object-level permissions: Users can always manage their own books
    Public/Private books: Control visibility of books
    Template integration: UI adapts based on user permissions


## Implementation Steps:

1. Run migrations to update your Book model
2. Execute the management command to create groups
3. Test the system by creating users and assigning them to different groups
4. Verify that permissions work correctly through the web interface

This implementation provides a complete permissions system for your bookshelf application using your existing CustomUser model and extending the Book model with the required permission structure.