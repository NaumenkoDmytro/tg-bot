# Generated by Django 4.2.4 on 2024-12-08 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0003_telegrambotconfig_channel_link_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="amazonmanualtask",
            name="start_time",
        ),
    ]
