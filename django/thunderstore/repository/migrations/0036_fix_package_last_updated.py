# Generated by Django 3.1.7 on 2022-07-28 11:49
from typing import Iterable, List, TypeVar

from django.db import migrations
from django.db.models import F, OuterRef, Q, Subquery

T = TypeVar("T")


def batch(batch_size: int, iterable: Iterable[T]) -> Iterable[List[T]]:
    collected = []
    for entry in iterable:
        collected.append(entry)
        if len(collected) >= batch_size:
            yield collected
            collected = []
    if len(collected) > 0:
        yield collected


def forwards(apps, schema_editor):
    Package = apps.get_model("repository", "Package")
    PackageVersion = apps.get_model("repository", "PackageVersion")
    for entry in batch(
        2000,
        Package.objects.exclude(
            Q(latest=None) | Q(date_updated=F("latest__date_created")),
        )
        .values_list("id", flat=True)
        .iterator(),
    ):
        Package.objects.filter(id__in=entry).update(
            date_updated=Subquery(
                PackageVersion.objects.filter(pk=OuterRef("latest")).values(
                    "date_created"
                )[:1]
            ),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0035_add_format_spec"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]