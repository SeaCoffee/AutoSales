from rest_framework.permissions import BasePermission, SAFE_METHODS


def get_user_role_name(user) -> str | None:
    role = getattr(user, 'role', None)

    if not role:
        return None

    return getattr(role, 'name', None)


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_authenticated)


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return get_user_role_name(user) == 'seller'


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return get_user_role_name(user) == 'buyer'


class IsPremiumAccount(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.account_type == 'premium'
        )


class IsPremiumSeller(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and get_user_role_name(user) == 'seller'
            and user.account_type == 'premium'
        )


class IsManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        role_name = get_user_role_name(user)

        return bool(
            user.is_staff
            and role_name in {'manager', 'admin'}
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.is_staff
            and user.is_superuser
        )


class IsSellerOrManagerAndOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        role_name = get_user_role_name(user)

        is_seller_and_owner = (
            role_name == 'seller'
            and getattr(obj, 'seller_id', None) == user.id
        )

        is_manager_or_admin = (
            user.is_staff
            and role_name in {'manager', 'admin'}
        )

        return is_seller_and_owner or is_manager_or_admin