from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from commons.enums import USER_TYPE, MOBILE
from .user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.CharField(
        max_length=150,
        unique=True,
        help_text=_('Different types of user uuid like Admin, Worker, Superuser')
    )
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(
        _('email address'),
        max_length=100,
        blank=True,
        null=True
    )
    company_uuid = models.CharField(max_length=150, blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    )
    user_type = models.CharField(choices=USER_TYPE, max_length=30, default=MOBILE)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_deleted = models.BooleanField(default=False, help_text=_('Uses for user soft delete'))

    objects = UserManager()

    USERNAME_FIELD = 'uuid'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
