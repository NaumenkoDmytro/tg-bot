# Generated by Django 4.2.4 on 2024-12-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0005_amazonautomationtask"),
    ]

    operations = [
        migrations.AddField(
            model_name="amazonautomationtask",
            name="keywords",
            field=models.CharField(default=" ", verbose_name="KeyWords"),
            preserve_default=False,
        ),
    ]