# Generated by Django 4.0.4 on 2022-05-24 20:19

from os import getenv

from django.db import migrations
from dotenv import load_dotenv

load_dotenv()


def default_user_admin(apps, schema_editor):

    Address = apps.get_model("addresses", "Address")
    Address.objects.create(
        id="ce45671c-d621-444c-9bbe-6ebd640b2059",
        street="Rua Pereira da Silva",
        complement="100 apto 502",
        city="Rio de Janeiro",
        state="Rio de Janeiro",
        zip_code="22345-029",
        country="Brasil",
    )

    User = apps.get_model("users", "User")
    User.objects.create_superuser(
        username=getenv("ADMIN_USERNAME"),
        email=getenv("ADMIN_EMAIL"),
        password=getenv("ADMIN_PASSWORD"),
        is_admin=True,
        first_name=getenv("ADMIN_USERNAME"),
        last_name="",
        cpf="11109876547",
        phone="5521987665842",
        address_id="ce45671c-d621-444c-9bbe-6ebd640b2059",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [migrations.RunPython(default_user_admin)]
