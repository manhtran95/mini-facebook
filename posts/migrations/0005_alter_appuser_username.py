# Generated by Django 4.1.7 on 2023-04-17 08:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_remove_appuser_app_username_alter_appuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(max_length=49, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]+$', 'Only alphanumeric characters are allowed.')]),
        ),
    ]
