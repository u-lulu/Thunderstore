from django.conf import settings
from django.db import models

from thunderstore.core.mixins import TimestampMixin


class ActiveManager(models.Manager):
    def active(self):
        return self.exclude(is_active=False)


class BaseReport(TimestampMixin):
    objects = ActiveManager()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)ss",
        on_delete=models.PROTECT,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
