from typing import Optional, Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from .models import UserProfile

UserModel = get_user_model()


class CustomAuthBackend(ModelBackend):
    """
    Custom authentication backend that checks if the user's account is active
    and handles role-based permissions.
    """

    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any,
    ) -> Optional[User]:
        """
        Authenticate a user and check if their account is active.

        Args:
            request: The current request
            username: The username to authenticate
            password: The password to verify
            **kwargs: Additional keyword arguments

        Returns:
            The authenticated user or None if authentication fails
        """
        if username is None or password is None:
            return None

        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # Run the default password hasher to mitigate timing attacks
            UserModel().set_password(password)
            return None

        if not user.check_password(password):
            return None

        if not self.user_can_authenticate(user):
            return None

        try:
            profile = user.profile
            if not profile.is_account_active:
                raise PermissionDenied("Your account is not yet activated.")
        except UserProfile.DoesNotExist:
            # If profile doesn't exist, create it
            UserProfile.objects.create(user=user)

        return user

    def has_perm(self, user_obj: User, perm: str, obj: Optional[Any] = None) -> bool:
        """
        Check if user has a specific permission.

        Args:
            user_obj: The user to check permissions for
            perm: The permission string to check
            obj: Optional object to check permissions against

        Returns:
            True if user has permission, False otherwise
        """
        if not user_obj.is_active:
            return False

        # Superusers have all permissions
        if user_obj.is_superuser:
            return True

        try:
            profile = user_obj.profile
        except UserProfile.DoesNotExist:
            return False

        # Role-based permissions
        if profile.role == "admin":
            return True
        elif profile.role == "officer":
            # Officers can do everything except user management
            if "auth." in perm:
                return False
            return True
        elif profile.role == "viewer":
            # Viewers can only view
            return perm.startswith("view_")

        return super().has_perm(user_obj, perm, obj)

    def get_user_permissions(
        self, user_obj: User, obj: Optional[Any] = None
    ) -> set[str]:
        """
        Get all permissions for a user.

        Args:
            user_obj: The user to get permissions for
            obj: Optional object to get permissions against

        Returns:
            Set of permission strings
        """
        if not user_obj.is_active:
            return set()

        try:
            profile = user_obj.profile
        except UserProfile.DoesNotExist:
            return set()

        perms = super().get_user_permissions(user_obj, obj)

        # Add role-based permissions
        if profile.role == "admin":
            perms.update(
                [
                    "tender_app.add_tender",
                    "tender_app.change_tender",
                    "tender_app.delete_tender",
                    "tender_app.view_tender",
                    "tender_app.can_approve_tender",
                    "tender_app.can_reject_tender",
                    "tender_app.view_all_tenders",
                ]
            )
        elif profile.role == "officer":
            perms.update(
                [
                    "tender_app.add_tender",
                    "tender_app.change_tender",
                    "tender_app.view_tender",
                ]
            )
        elif profile.role == "viewer":
            perms.add("tender_app.view_tender")

        return perms
