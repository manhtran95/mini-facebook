# Generated by Django 4.1.7 on 2023-04-30 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_appuser_cover_photo_appuser_profile_picture')]

    database_operations = [
        migrations.AlterModelTable('AppUser', 'users_appuser')
    ]

    state_operations = [
        migrations.DeleteModel('AppUser')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]
