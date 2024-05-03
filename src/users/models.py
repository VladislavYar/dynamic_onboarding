from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class User(AbstractUser):
    """Кастомный пользователь."""

    email = models.EmailField(
        unique=True,
        verbose_name=_('Email'),
        help_text=_('Email'),
        db_comment=_('Email'),
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    username = None

    class Meta(AbstractUser.Meta):
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')
