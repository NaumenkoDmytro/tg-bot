# Generated by Django 4.2.4 on 2024-12-16 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0010_amazonsavedproducts"),
    ]

    operations = [
        migrations.CreateModel(
            name="AliExpressSavedProducts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField()),
                ("product_link", models.CharField()),
                ("video_url", models.CharField()),
                ("price", models.CharField()),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="alik_saved_products",
                        to="main_app.aliexpressautomationtask",
                    ),
                ),
            ],
        ),
    ]
