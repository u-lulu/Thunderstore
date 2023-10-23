from django.db import models

from thunderstore.core.mixins import TimestampMixin
from thunderstore.reports.models.base import ActiveManager


class PackageReportReason(TimestampMixin):
    objects = ActiveManager()

    label = models.TextField()
    is_active = models.BooleanField(default=True)
