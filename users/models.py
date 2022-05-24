import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):

        now = timezone.now()

        if not email:
            raise ValueError("The given email must be set.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    is_admin = models.BooleanField(default=False)
    cpf = models.CharField(max_length=11, unique=True, null=False)
    phone = models.CharField(max_length=50, null=False)
    rental_active = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    address = models.ForeignKey(
        'addresses.Address', on_delete=models.CASCADE, related_name='users', null=True
    )    

USERNAME_FIELD = 'email'
REQUIRED_FIELDS = []

objects = CustomUserManager()
