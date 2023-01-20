# Generated by Django 4.0 on 2022-10-16 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(default='images/default.png', upload_to='products/%Y/%m/%d/')),
                ('facebook', models.URLField(blank=True, max_length=100)),
                ('twitter', models.URLField(blank=True, max_length=100)),
                ('linkedin', models.URLField(blank=True, max_length=100)),
                ('youtube', models.URLField(blank=True, max_length=100)),
                ('is_seller', models.BooleanField(default=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
