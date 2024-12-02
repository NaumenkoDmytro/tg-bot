# Generated by Django 4.2.4 on 2024-12-01 12:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0006_amazonautomationtask_keywords"),
    ]

    operations = [
        migrations.AddField(
            model_name="amazonautomationtask",
            name="num_items",
            field=models.IntegerField(default=1, verbose_name="Number of Items"),
        ),
        migrations.AlterField(
            model_name="amazonautomationtask",
            name="keywords",
            field=models.CharField(
                help_text="Min: 1, Max: 10",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(10),
                ],
                verbose_name="KeyWords",
            ),
        ),
    ]
