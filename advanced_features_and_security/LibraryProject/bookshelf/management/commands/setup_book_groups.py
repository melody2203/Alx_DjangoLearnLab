from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create default groups and assign book permissions'

    def handle(self, *args, **options):
        # Get content type for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Create Viewers group - can only view books
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        can_view = Permission.objects.get(codename='can_view', content_type=content_type)
        viewers_group.permissions.add(can_view)
        self.stdout.write(
            self.style.SUCCESS('Successfully created Viewers group with can_view permission')
        )

        # Create Editors group - can view, create, and edit books
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editor_perms = ['can_view', 'can_create', 'can_edit']
        for perm_name in editor_perms:
            perm = Permission.objects.get(codename=perm_name, content_type=content_type)
            editors_group.permissions.add(perm)
        self.stdout.write(
            self.style.SUCCESS('Successfully created Editors group with can_view, can_create, can_edit permissions')
        )

        # Create Admins group - all permissions including delete
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admin_perms = ['can_view', 'can_create', 'can_edit', 'can_delete']
        for perm_name in admin_perms:
            perm = Permission.objects.get(codename=perm_name, content_type=content_type)
            admins_group.permissions.add(perm)
        self.stdout.write(
            self.style.SUCCESS('Successfully created Admins group with all permissions')
        )