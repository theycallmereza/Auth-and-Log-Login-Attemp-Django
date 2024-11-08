from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verification/code/', views.IssueVerficationCodeView.as_view(), name='verification_code'),
    path('verification/code/verify/', views.VerifyEmailWithCode.as_view(), name='verification_code_verify'),
]
