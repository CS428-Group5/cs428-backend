# Generated by Django 4.2.2 on 2023-08-09 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0010_bookedsession_booked_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookedsession',
            name='booked_price',
        ),
        migrations.AddField(
            model_name='mentorsession',
            name='session_price',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=13, null=True),
        ),
    ]
