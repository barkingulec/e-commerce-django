# Generated by Django 4.0 on 2022-10-17 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_alter_profile_first_name_alter_profile_last_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='linkedin',
            new_name='instagram',
        ),
    ]