# Generated by Django 4.2.2 on 2023-07-15 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_delete_favorite"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="mentee_id",
            new_name="mentee",
        ),
        migrations.RenameField(
            model_name="review",
            old_name="mentor_id",
            new_name="mentor",
        ),
        migrations.AlterField(
            model_name="mentee",
            name="favorites",
            field=models.ManyToManyField(
                blank=True, related_name="favorites", to="users.mentor"
            ),
        ),
    ]
