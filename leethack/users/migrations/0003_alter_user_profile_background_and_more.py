# Generated by Django 5.2.1 on 2025-06-01 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_profile_background_user_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_background",
            field=models.ImageField(
                blank=True,
                default="profile_backgrounds/default.jpg",
                upload_to="profile_backgrounds/",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="profile_pictures/default.png",
                upload_to="profile_pictures/",
            ),
        ),
    ]
