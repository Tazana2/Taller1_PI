# Generated by Django 5.0.7 on 2024-08-21 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="date",
            field=models.DateField(),
        ),
    ]
