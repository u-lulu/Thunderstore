# Generated by Django 3.1.7 on 2022-02-02 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0018_add_package_rejection_reason"),
    ]

    operations = [
        migrations.AddField(
            model_name="communitysite",
            name="is_pre_subdomain_change_site",
            field=models.BooleanField(default=False),
        ),
    ]
