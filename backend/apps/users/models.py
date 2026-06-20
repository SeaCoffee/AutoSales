from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models

from core.enums.regex_enum import RegexEnum
from core.models import BaseModel
from core.services.upload_photos import upload_avatar
from apps.users_auth.models import UserRoleModel

from apps.users.manager import UserManager


class AccountType(models.TextChoices):
    BASIC = 'basic', 'Basic'
    PREMIUM = 'premium', 'Premium'


class UserModel(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=55, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(
        UserRoleModel,
        on_delete=models.PROTECT,
        related_name='users',
    )
    account_type = models.CharField(
        max_length=10,
        choices=AccountType.choices,
        default=AccountType.BASIC,
    )
    is_upgrade_to_premium = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = 'custom_auth_user'
        ordering = ('-created_at',)

    def __str__(self):
        return self.username


class ProfileModel(BaseModel):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    name = models.CharField(
        max_length=55,
        blank=True,
        default='',
        validators=[validators.RegexValidator(*RegexEnum.NAME.value)],
    )
    surname = models.CharField(
        max_length=55,
        blank=True,
        default='',
        validators=[validators.RegexValidator(*RegexEnum.NAME.value)],
    )
    age = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(16),
            validators.MaxValueValidator(100),
        ],
        null=True,
        blank=True,
    )
    city = models.CharField(max_length=100, blank=True, default='')
    avatar = models.ImageField(
        upload_to=upload_avatar,
        blank=True,
        null=True,
        validators=[
            validators.FileExtensionValidator(['jpeg', 'jpg', 'png', 'webp']),
        ],
    )

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return f'{self.user.username} profile'


class BlacklistModel(BaseModel):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='blacklist_entry',
    )
    added_by = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='added_blacklist_entries',
    )
    reason = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'blacklist'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user.username} blacklist entry'