from django.core.exceptions import ValidationError
from django.db import models

from thunderstore.reports.models.base import BaseReport


class PackageReport(BaseReport):
    package_listing = models.ForeignKey(
        "repository.PackageListing",
        related_name="reports",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    package_version = models.ForeignKey(
        "repository.PackageVersion",
        related_name="reports",
        on_delete=models.CASCADE,
    )
    reason = models.ForeignKey(
        "ts_reports.PackageReportReason",
        related_name="reports",
        on_delete=models.PROTECT,
    )

    def validate(self):
        if self.package_listing.package != self.package_version.package:
            raise ValidationError("Package mismatch!")

    def save(self, *args, **kwargs):
        self.validate()
        return super().save(*args, **kwargs)
