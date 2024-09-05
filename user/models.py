from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields = {"is_staff": False, "is_superuser": False, **extra_fields}
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields = {
            "is_cse": True,
            "is_ece": True,
            "is_eee": True,
            "is_mech": True,
            "is_csse": True,
            "is_csit": True,
            "is_csm": True,
            "is_student": False,
            "is_staff": True,
            "is_superuser": True,
            **extra_fields,
        }

        user = self.create_user(email=email, password=password, **extra_fields)
        return user


class User(AbstractUser):
    username = None
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    is_cse = models.BooleanField(default=False)
    is_ece = models.BooleanField(default=False)
    is_eee = models.BooleanField(default=False)
    is_mech = models.BooleanField(default=False)
    is_csse = models.BooleanField(default=False)
    is_csit = models.BooleanField(default=False)
    is_csm = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    reg_no = models.CharField(max_length=10, blank=True, null=True, unique=True)
    batch_year = models.CharField(max_length=4, blank=True, null=True)
    batch = models.CharField(max_length=6, blank=True, null=True)
    tests = models.JSONField(blank=True, null=True)
    drives = models.JSONField(blank=True, null=True)
    documents = models.ManyToManyField(
        "home.Document", related_name="users"
    )  # Use string reference

    objects = UserManager()

    def __str__(self):
        return self.email
