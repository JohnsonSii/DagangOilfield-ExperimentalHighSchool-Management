# Generated by Django 4.2.3 on 2023-08-20 11:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("username", models.CharField(max_length=20, null=True)),
                ("password", models.CharField(max_length=50, null=True)),
                ("role", models.IntegerField(null=True)),
                ("name", models.CharField(max_length=10, null=True)),
                ("qq", models.CharField(max_length=20, null=True)),
                ("school", models.CharField(max_length=20, null=True)),
                ("image_url", models.CharField(max_length=100, null=True)),
                ("passed", models.IntegerField(null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]