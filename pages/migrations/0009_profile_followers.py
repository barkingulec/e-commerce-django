# Generated by Django 4.0 on 2022-10-21 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(to='pages.Follow'),
        ),
    ]