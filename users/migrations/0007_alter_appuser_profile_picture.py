# Generated by Django 4.1.7 on 2023-05-03 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_appuser_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='profile_picture',
            field=models.ImageField(
                default='media/profile_pictures/default-profile-picture_xdklkn.jpg', null=True, upload_to='profile_pictures'),
        ),
    ]
