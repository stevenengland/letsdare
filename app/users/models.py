from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as Bum
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from app.common.models import BaseModel

# Taken from here:
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
# With some modifications


class BaseUserManager(Bum):  # type: ignore[type-arg]
    """The base user manager."""

    def create_user(self, email, is_active=True, is_admin=False, password=None):
        """Create a new user."""
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            is_admin=is_admin,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Create a superuser."""
        user = self.create_user(  # type: ignore[no-untyped-call]
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    """The base user."""

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,  # noqa: WPS432
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()  # noqa: WPS110

    USERNAME_FIELD = "email"  # noqa: WPS115

    def __str__(self):
        """Override __str__."""
        return self.email

    def is_staff(self):
        """Override is_staff."""
        return self.is_admin
