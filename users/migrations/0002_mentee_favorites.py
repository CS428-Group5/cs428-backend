# Generated by Django 4.2.2 on 2023-07-08 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="mentee",
            name="favorites",
            field=models.ManyToManyField(related_name="favorites", to="users.mentor"),
        ),
    ]
