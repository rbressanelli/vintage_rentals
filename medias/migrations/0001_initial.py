# Generated by Django 4.0.4 on 2022-05-24 19:30

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Media",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
                ("release_year", models.CharField(max_length=4)),
                ("genre", models.CharField(max_length=100)),
                (
                    "media_type",
                    models.CharField(
                        choices=[
                            ("LP", "Long Play"),
                            ("K7", "Fita Cassete"),
                            ("VHS", "Fita de Vídeo"),
                        ],
                        max_length=3,
                    ),
                ),
                ("director", models.CharField(max_length=255)),
                ("artist", models.CharField(max_length=255)),
                ("rental_price_per_day", models.FloatField()),
                ("condition", models.CharField(default=None, max_length=255)),
                ("available", models.BooleanField(default=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
