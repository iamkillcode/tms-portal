from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Set up user roles and assign permissions for TMS.'

    def handle(self, *args, **options):
        # Define roles
        roles = [
            'Admin',
            'Head of Department',
            'Head of Unit',
            'Team Lead',
            'Officer',
        ]
        # Create groups if they don't exist
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {role}'))

        # Assign permissions
        all_perms = Permission.objects.all()
        admin_perms = all_perms
        user_perms = Permission.objects.filter(codename__in=[
            'view_tender', 'add_tender', 'change_tender', 'view_userprofile',
            'view_task', 'add_task', 'change_task', 'view_frameworkagreement',
            'view_vendorbid', 'add_vendorbid', 'change_vendorbid',
        ])

        # Admin, Head of Department, Head of Unit: all permissions
        for role in ['Admin', 'Head of Department', 'Head of Unit']:
            group = Group.objects.get(name=role)
            group.permissions.set(admin_perms)
            self.stdout.write(self.style.SUCCESS(f'Assigned all permissions to {role}'))

        # Team Lead, Officer: user permissions
        for role in ['Team Lead', 'Officer']:
            group = Group.objects.get(name=role)
            group.permissions.set(user_perms)
            self.stdout.write(self.style.SUCCESS(f'Assigned user permissions to {role}'))

        self.stdout.write(self.style.SUCCESS('Roles and permissions setup complete.'))
