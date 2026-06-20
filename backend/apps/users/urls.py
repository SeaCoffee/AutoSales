from django.urls import path

from apps.users.views import (
    BlacklistManageView,
    CreateManagerView,
    CurrentUserDetailsView,
    PremiumRequestAPIView,
    ProfileDetailView,
    ProfileUpdateView,
    UserAvatarUpdateAPIView,
    UserCreateAPIView,
    UserDeleteSelfView,
)


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('me/', CurrentUserDetailsView.as_view(), name='current-user'),
    path('me/profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('me/profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('me/avatar/', UserAvatarUpdateAPIView.as_view(), name='profile-avatar'),
    path('me/premium-request/', PremiumRequestAPIView.as_view(), name='premium-request'),
    path('me/delete/', UserDeleteSelfView.as_view(), name='user-delete-self'),
    path('managers/', CreateManagerView.as_view(), name='manager-create'),
    path('blacklist/', BlacklistManageView.as_view(), name='blacklist-manage'),
]