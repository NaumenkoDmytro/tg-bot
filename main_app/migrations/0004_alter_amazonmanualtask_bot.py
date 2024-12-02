# Generated by Django 4.2.4 on 2024-11-26 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0003_amazonmanualtask_bot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="amazonmanualtask",
            name="bot",
            field=models.ManyToManyField(
                to="main_app.telegrambotconfig", verbose_name="Telegram Bot Configs"
            ),
        ),
    ]