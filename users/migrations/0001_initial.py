# Generated by Django 5.1 on 2024-08-14 16:44

import core.services.upload_photos
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=55, unique=True)),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator('^(?=.*\\d)(?=.*[a-zA-Z])(?=.*[\\W\\d\\s:])([^\\s]){8,16}$', ['password must contain 1 number (0 - 9)', 'password must contain 1 uppercase letters', 'password must contain 1 lowercase letters', 'password must contain 1 non - alpha numeric number', 'password is 8 - 16 characters with no space'])])),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('account_type', models.CharField(choices=[('basic', 'Basic'), ('premium', 'Premium')], default='basic', max_length=10)),
                ('is_upgrade_to_premium', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('role', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='users_auth.userrolemodel')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'custom_auth_user',
            },
        ),
        migrations.CreateModel(
            name='BlacklistModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='added_blacklist_entries', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='blacklist_entry', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=55, validators=[django.core.validators.RegexValidator('^[A-Z][a-zA-Z]{1,19}$', 'First letter uppercase min 2 max 20 ch')])),
                ('surname', models.CharField(max_length=55, validators=[django.core.validators.RegexValidator('^[A-Z][a-zA-Z]{1,19}$', 'First letter uppercase min 2 max 20 ch')])),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(16), django.core.validators.MaxValueValidator(100)])),
                ('city', models.CharField(max_length=100)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=core.services.upload_photos.upload_avatar, validators=[django.core.validators.FileExtensionValidator(['jpeg', 'jpg', 'png'])])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
    ]
