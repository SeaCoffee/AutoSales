from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView,
    ResetPasswordAPIView,
    RoleListAPIView,
    SocketTokenAPIView,
    UserActivateAPIView,
    UserRecoverAPIView,
)


urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='user-auth-login'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('activate/<str:token>/', UserActivateAPIView.as_view(), name='activate-account'),
    path('password/recovery/', UserRecoverAPIView.as_view(), name='password-recovery'),
    path('password/reset/<str:token>/', ResetPasswordAPIView.as_view(), name='password-reset'),
    path('roles/', RoleListAPIView.as_view(), name='role-list'),
    path('socket/', SocketTokenAPIView.as_view(), name='socket-token'),
]