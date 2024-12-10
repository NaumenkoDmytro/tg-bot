# Generated by Django 4.2.4 on 2024-12-08 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0004_remove_amazonmanualtask_start_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aliexpressapi",
            name="api_token",
        ),
        migrations.AddField(
            model_name="aliexpressapi",
            name="app_key",
            field=models.CharField(
                default=" ", max_length=300, verbose_name="AliExpress App Key"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="aliexpressapi",
            name="secret_key",
            field=models.CharField(
                default=" ", max_length=300, verbose_name="AliExpress Secret Key"
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="AliExpressManualTask",
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
                    "product_codes",
                    models.JSONField(
                        default=list,
                        help_text='The field must be empty, for example: [] or contain a list of product code\'s in the following JSON format: ["CODE", "CODE"].',
                        verbose_name="AliExpress Product Codes",
                    ),
                ),
                (
                    "aliexpress_api",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks_aliexpress_api",
                        to="main_app.aliexpressapi",
                        verbose_name="AliExpress Credentials",
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
                "verbose_name": "AliExpress Task",
                "verbose_name_plural": "AliExpress Tasks",
            },
        ),
    ]
