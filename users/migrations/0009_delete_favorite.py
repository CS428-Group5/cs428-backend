# Generated by Django 4.2.2 on 2023-07-13 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_mentor_experience_review_favorite"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Favorite",
        ),
    ]
