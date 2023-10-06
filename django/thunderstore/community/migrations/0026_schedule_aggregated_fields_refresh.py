# Generated by Django 3.1.7 on 2023-10-18 09:40

import pytz
from django.db import migrations


def forwards(apps, schema_editor):
    CrontabSchedule = apps.get_model("django_celery_beat", "CrontabSchedule")
    PeriodicTask = apps.get_model("django_celery_beat", "PeriodicTask")

    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="1",
        hour="*",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
        timezone=pytz.timezone("UTC"),
    )
    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name="Update CommunityAggregatedFields",
        task="thunderstore.community.tasks.update_community_aggregated_fields",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0025_init_aggregated_fields"),
        ("django_celery_beat", "0014_remove_clockedschedule_enabled"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
