from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, imap_password, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, imap_password=imap_password, **extra_fields)
        user.set_password(password)  # Hash the regular password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, imap_password, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, imap_password, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    email = models.EmailField(unique=True)
    imap_password = models.CharField(max_length=128)  # Store IMAP password as plain text or encrypted
    hours_worked = models.JSONField(default=list)  # Stores list of worked hours per day
    orders_taken = models.JSONField(default=list)  # Stores list of orders per day
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["imap_password"]

    def __str__(self):
        return self.email
