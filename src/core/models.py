from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.constants import MAX_LEN_NAME, MAX_LEN_SLUG


class BaseModel(models.Model):
    """Базовая модель."""

    name = models.CharField(
        max_length=MAX_LEN_NAME,
        verbose_name=_('Название'),
        help_text=_('Название'),
        db_comment=_('Название'),
    )
    slug = AutoSlugField(
        max_length=MAX_LEN_SLUG,
        verbose_name=_('Slug-название'),
        help_text=_('Slug-название'),
        db_comment=_('Slug-название'),
        unique=True,
        db_index=True,
        populate_from='name',
        always_update=True,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.name} | {self.slug}'
