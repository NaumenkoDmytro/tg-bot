# Generated by Django 4.2.4 on 2024-11-26 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0002_remove_amazonapi_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="amazonmanualtask",
            name="bot",
            field=models.ManyToManyField(to="main_app.telegrambotconfig"),
        ),
    ]
