from django.contrib.auth.models import User
from tender_app.models import UserProfile

def create_missing_profiles():
    for user in User.objects.all():
        if not hasattr(user, 'profile'):
            UserProfile.objects.create(
                user=user,
                full_name=f"{user.first_name} {user.last_name}".strip() or user.username
            )

if __name__ == '__main__':
    create_missing_profiles()