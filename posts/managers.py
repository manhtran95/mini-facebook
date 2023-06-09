from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import re
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator, NumericPasswordValidator
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email and password.
        """
        if not re.match(r'^[0-9a-zA-Z]+$', username):
            raise ValueError(
                _('Only allow alphanumeric characters for username!'))
        email = self.normalize_email(email)
        validate_email(email)
        validate_password(password, password_validators=[
                          MinimumLengthValidator(min_length=6), NumericPasswordValidator()])
        user = self.model(username=username,
                          email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, email, password, **extra_fields)
