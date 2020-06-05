from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView

import authentication.views as api_views

urlpatterns = [
    path('signup/', api_views.SignupView.as_view()),
    path('login/', api_views.LoginView.as_view()),
    path('reset/', api_views.ChangeCredentialsView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('me/', api_views.UserInformationView.as_view()),
    path('forgot/', api_views.ForgotPasswordView.as_view()),
    path('verify/', api_views.VerifyEmailView.as_view()),
    path('2fa/', api_views.TwoFactorView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)