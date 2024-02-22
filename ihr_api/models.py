from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    ROLE_ADMIN = 0
    ROLE_STORE_ADMIN = 1
    ROLE_CLIENT = 2

    Roles = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_STORE_ADMIN, 'Store Admin'),
        (ROLE_CLIENT, 'Client'),
    )

    role = models.IntegerField(null=False, choices=Roles, default=ROLE_CLIENT, blank=False)
