# core/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .auth_views import (
    RegisterView, EmailVerificationView, PhoneVerificationView,
    PasswordResetRequestView, PasswordResetConfirmView,
    EmailLoginView, PhoneLoginView, GoogleLoginView,
    ResendVerificationView
)
from .profile_views import (
    UserProfileView, AssistantProfileView, UpdateLocationView,
    AssistantStatusView, AssistantListView
)

urlpatterns = [
    # Authentication URLs
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/verify-email/', EmailVerificationView.as_view(), name='verify-email'),
    path('auth/verify-phone/', PhoneVerificationView.as_view(), name='verify-phone'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/login/email/', EmailLoginView.as_view(), name='login-email'),
    path('auth/login/phone/', PhoneLoginView.as_view(), name='login-phone'),
    path('auth/login/google/', GoogleLoginView.as_view(), name='login-google'),
    path('auth/resend-verification/', ResendVerificationView.as_view(), name='resend-verification'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Profile URLs
    path('profile/user/', UserProfileView.as_view(), name='user-profile'),
    path('profile/assistant/', AssistantProfileView.as_view(), name='assistant-profile'),
    path('profile/update-location/', UpdateLocationView.as_view(), name='update-location'),
    path('profile/assistant-status/', AssistantStatusView.as_view(), name='assistant-status'),
    path('assistants/', AssistantListView.as_view(), name='assistant-list'),
]