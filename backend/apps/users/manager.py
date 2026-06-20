from django.apps import apps
from django.contrib.auth.models import BaseUserManager
from django.db.transaction import atomic

from apps.users_auth.models import UserRoleModel


class UserManager(BaseUserManager):
    default_user_role = 'buyer'
    manager_role = 'manager'
    admin_role = 'admin'

    def get_role(self, role=None, default_role_name: str | None = None):
        if isinstance(role, UserRoleModel):
            return role

        if isinstance(role, int):
            return UserRoleModel.objects.get(pk=role)

        if isinstance(role, str):
            role_obj, _ = UserRoleModel.objects.get_or_create(name=role)
            return role_obj

        role_name = default_role_name or self.default_user_role
        role_obj, _ = UserRoleModel.objects.get_or_create(name=role_name)

        return role_obj

    @atomic
    def create_user(
        self,
        email,
        username,
        password=None,
        role=None,
        account_type='basic',
        profile_data=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError('Email is required.')

        if not username:
            raise ValueError('Username is required.')

        if not password:
            raise ValueError('Password is required.')

        email = self.normalize_email(email)
        user_role = self.get_role(role, self.default_user_role)

        user = self.model(
            email=email,
            username=username,
            role=user_role,
            account_type=account_type,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        if not user.is_superuser:
            ProfileModel = apps.get_model('users', 'ProfileModel')
            ProfileModel.objects.create(user=user, **(profile_data or {}))

        return user

    @atomic
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self.create_user(
            email=email,
            username=username,
            password=password,
            role=self.admin_role,
            account_type='premium',
            **extra_fields,
        )

    @atomic
    def create_manager(
        self,
        creator_user,
        email,
        username,
        password=None,
        profile_data=None,
        **extra_fields,
    ):
        creator_role_name = getattr(getattr(creator_user, 'role', None), 'name', None)

        can_create_manager = (
            creator_user
            and creator_user.is_authenticated
            and (
                creator_user.is_superuser
                or (creator_user.is_staff and creator_role_name == self.admin_role)
            )
        )

        if not can_create_manager:
            raise PermissionError('Only superusers or admins can create managers.')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Manager must have is_staff=True.')

        if extra_fields.get('is_active') is not True:
            raise ValueError('Manager must have is_active=True.')

        return self.create_user(
            email=email,
            username=username,
            password=password,
            role=self.manager_role,
            account_type='premium',
            profile_data=profile_data,
            **extra_fields,
        )

    @atomic
    def delete_own_user(self, user):
        if not user or not self.model.objects.filter(id=user.id).exists():
            raise ValueError('User with given ID does not exist.')

        user.delete()

        return 'Your account has been deleted successfully.'