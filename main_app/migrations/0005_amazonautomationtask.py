# Generated by Django 4.2.4 on 2024-12-01 12:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0004_alter_amazonmanualtask_bot"),
    ]

    operations = [
        migrations.CreateModel(
            name="AmazonAutomationTask",
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
                ("name", models.CharField(max_length=150, verbose_name="Task Name")),
                (
                    "status",
                    models.CharField(
                        choices=[("New", "New"), ("Done", "Done")],
                        default="New",
                        max_length=10,
                        verbose_name="Task Status",
                    ),
                ),
                (
                    "min_price",
                    models.IntegerField(
                        default=0,
                        help_text="Filters search results to items with at least one offer price above the specified value. Prices appear in lowest currency denomination. For example, $31.41 should be passed as 3141 or 28.00€ should be 2800.",
                        verbose_name="Min Price",
                    ),
                ),
                (
                    "max_price",
                    models.IntegerField(
                        default=0,
                        help_text="Filters search results to items with at least one offer price above the specified value. Prices appear in lowest currency denomination. For example, $31.41 should be passed as 3141 or 28.00€ should be 2800.",
                        verbose_name="Max Price",
                    ),
                ),
                (
                    "start_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Start Time"
                    ),
                ),
                (
                    "amazon_api",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auto_tasks_amazon_api",
                        to="main_app.amazonapi",
                        verbose_name="Amazon API Credentials",
                    ),
                ),
                (
                    "bot",
                    models.ManyToManyField(
                        to="main_app.telegrambotconfig",
                        verbose_name="Telegram Bot Configs",
                    ),
                ),
            ],
            options={
                "verbose_name": "Amazon Automation Task",
                "verbose_name_plural": "Amazon Automation Tasks",
            },
        ),
    ]