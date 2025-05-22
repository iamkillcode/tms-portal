from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

def setup_roles():
    # Create groups
    roles = [
        "Admin", "Head of Department", "Head of Unit", "Team Lead", "Officer"
    ]
    for role in roles:
        Group.objects.get_or_create(name=role)

    # Assign permissions (example: all permissions for admin)
    admin_group = Group.objects.get(name="Admin")
    all_permissions = Permission.objects.all()
    admin_group.permissions.set(all_permissions)

    # Head of Department/Unit: same as admin
    for role in ["Head of Department", "Head of Unit"]:
        group = Group.objects.get(name=role)
        group.permissions.set(all_permissions)

    # Team Lead/Officer: basic permissions
    basic_perms = Permission.objects.filter(codename__in=[
        "view_tender", "add_tender", "change_tender", "view_userprofile"
    ])
    for role in ["Team Lead", "Officer"]:
        group = Group.objects.get(name=role)
        group.permissions.set(basic_perms)