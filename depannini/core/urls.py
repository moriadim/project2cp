# core/urls.py
from django.urls import path


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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .assistance_views import (
    AssistanceRequestView,
    AssistanceListDetailView,
    AcceptAssistanceView,
    AssistanceUpdateView,

)

urlpatterns = [
    # Authentication URLs
    path('auth/register/', RegisterView.as_view(), name='register'),  # done
    path('auth/verify-email/', EmailVerificationView.as_view(), name='verify-email'),
    path('auth/verify-phone/', PhoneVerificationView.as_view(), name='verify-phone'),
    path(
        'auth/password-reset/',
        PasswordResetRequestView.as_view(), name='password-reset'
    ),
    path(
        'auth/password-reset/confirm/',
        PasswordResetConfirmView.as_view(), name='password-reset-confirm'
    ),
    path(
        'auth/login/email/', EmailLoginView.as_view(),
        name='login-email'
    ),  # done
    path(
        'auth/login/phone/', PhoneLoginView.as_view(),
        name='login-phone'
    ),  # done
    path('auth/login/google/', GoogleLoginView.as_view(), name='login-google'),
    path(
        'auth/resend-verification/',
        ResendVerificationView.as_view(), name='resend-verification'
    ),
    path(
        'auth/token/refresh/', TokenRefreshView.as_view(),
        name='token-refresh'
    ),  # done
    path(
        'token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),  # done
    path(
        'token/refresh/', TokenRefreshView.as_view(),
        name='token_refresh'
    ),  # done

    # Profile URLs
    path(
        'profile/user/', UserProfileView.as_view(), name='user-profile'
    ),
    path(
        'profile/assistant/', AssistantProfileView.as_view(),
        name='assistant-profile'
    ),
    path(
        'profile/update-location/',
        UpdateLocationView.as_view(), name='update-location'
    ),
    path(
        'profile/assistant-status/',
        AssistantStatusView.as_view(), name='assistant-status'
    ),
    path('assistants/', AssistantListView.as_view(), name='assistant-list'),

    # Assistance URLs

    path(
        'assistance/request/', AssistanceRequestView.as_view(),
        name='assistance-request'
    ),
    path(
        'assistance/view/', AssistanceListDetailView.as_view(),
        name='assistance-view'
    ),
    path(
        'assistance/view/<int:assistance_id>/', AssistanceListDetailView.as_view(),
        name='assistance-view'
    ),
    path(
        'assistance/accept/<int:assistance_id>/', AcceptAssistanceView.as_view(),
        name='assistance-accept'
    ),
    path(
        'assistance/update/<int:assistance_id>/', AssistanceUpdateView.as_view(),
        name='status-update'
    ),
]
