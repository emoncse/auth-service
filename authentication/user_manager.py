from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, uuid, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given uuid and password.
        """
        now = timezone.now()
        if not uuid:
            raise ValueError('The given uuid must be set')
        user = self.model(
            uuid=uuid,
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

    def create_user(self, uuid, password=None, **extra_fields):
        return self._create_user(uuid, password, False, False, **extra_fields)

    def create_superuser(self, uuid, password, **extra_fields):
        return self._create_user(uuid, password, True, True, **extra_fields)
