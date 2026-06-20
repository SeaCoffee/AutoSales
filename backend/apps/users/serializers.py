from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import serializers

from apps.users.models import BlacklistModel, ProfileModel
from apps.users_auth.models import UserRoleModel
from core.services.email_service import EmailService
from core.validators.users_validators import (
    normalize_email,
    validate_avatar_file_size,
    validate_blacklist_target,
    validate_password_strength,
)


UserModel = get_user_model()


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleModel
        fields = ('id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='user.role.name', read_only=True)
    account_type = serializers.CharField(source='user.account_type', read_only=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = ProfileModel
        fields = (
            'id',
            'name',
            'surname',
            'age',
            'city',
            'role',
            'account_type',
            'avatar',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'role',
            'account_type',
            'avatar',
            'created_at',
            'updated_at',
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('name', 'surname', 'age', 'city')


class CurrentUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', read_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = UserModel
        fields = (
            'id',
            'email',
            'username',
            'role',
            'account_type',
            'is_upgrade_to_premium',
            'profile',
            'created_at',
            'updated_at',
        )
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer(required=False)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = UserModel
        fields = (
            'id',
            'email',
            'username',
            'password',
            'profile',
        )
        read_only_fields = ('id',)

    def validate_email(self, value):
        return normalize_email(value)

    def validate_password(self, value):
        return validate_password_strength(value)

    @atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)

        user = UserModel.objects.create_user(
            profile_data=profile_data,
            **validated_data,
        )

        EmailService.register(user)

        return user


class PremiumRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('is_upgrade_to_premium',)
        read_only_fields = ('is_upgrade_to_premium',)

    def update(self, instance, validated_data):
        instance.is_upgrade_to_premium = True
        instance.save(update_fields=('is_upgrade_to_premium', 'updated_at'))

        return instance


class ManagerCreateSerializer(serializers.ModelSerializer):
    profile = ProfileUpdateSerializer(required=False)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = UserModel
        fields = (
            'id',
            'email',
            'username',
            'password',
            'profile',
        )
        read_only_fields = ('id',)

    def validate_email(self, value):
        return normalize_email(value)

    def validate_password(self, value):
        return validate_password_strength(value)

    @atomic
    def create(self, validated_data):
        request = self.context.get('request')

        if not request:
            raise serializers.ValidationError('Request context is required.')

        profile_data = validated_data.pop('profile', None)

        try:
            return UserModel.objects.create_manager(
                creator_user=request.user,
                profile_data=profile_data,
                **validated_data,
            )
        except PermissionError as error:
            raise serializers.ValidationError(str(error)) from error


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('avatar',)

    def validate_avatar(self, avatar):
        return validate_avatar_file_size(avatar)


class BlacklistSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)

    class Meta:
        model = BlacklistModel
        fields = (
            'id',
            'user',
            'username',
            'added_by',
            'added_by_username',
            'reason',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'username',
            'added_by',
            'added_by_username',
            'created_at',
            'updated_at',
        )


class AddToBlacklistSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        request = self.context.get('request')
        request_user = request.user if request else None

        attrs['user'] = validate_blacklist_target(
            target_user_id=attrs['user_id'],
            request_user=request_user,
        )

        return attrs