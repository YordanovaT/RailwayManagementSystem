from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.


class CustomUserManager(BaseUserManager):
    """This is the CustomUserManager class for the users."""

    def _create_user(self, email, password, first_name, last_name, mobile,
                     **extra_fields):  # pylint:disable=too-many-arguments
        if not email:
            raise ValueError("Email must be provided.")
        if not password:
            raise ValueError("Password must be provided.")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            **extra_fields
        )
        user.set_password(password)  # This is how password is hashed
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, mobile,
                    **extra_fields):  # pylint:disable=too-many-arguments
        """This method is used when creating user."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, mobile,
                         **extra_fields):  # pylint:disable=too-many-arguments
        """This method is used when creating superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """This is the class used for the users."""
    email = models.EmailField(db_index=True, unique=True, max_length=150)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    # need that so we can be able to log into django-admin

    is_active = models.BooleanField(default=True)
    # this is needed for the same reason
    is_superuser = models.BooleanField(default=False)
    # This field is inherited from the PermissionsMixin

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']

    class Meta:  # pylint:disable=too-few-public-methods
        """This is the Meta class for the user."""
        verbose_name = 'User'
        verbose_name_plural = 'Users'
