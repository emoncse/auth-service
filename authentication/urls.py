from django.urls import path
from .views import (
    WorkersView,
    JSONWebTokenWebAuth,
    JSONWebTokenMobileAuth,
    TokenVerifyView,
    LogoutView,
    ChangePasswordView,
    PasswordReGenerateView,
    CodeGenerateByIDView,
    AdminsViews,
    VerifyCodeAndCreateAccessTokenView,
    SetNewPasswordView
)

urlpatterns = [
    path('web/login', JSONWebTokenWebAuth.as_view(), name='web-user-login'),
    path('mobile/login', JSONWebTokenMobileAuth.as_view(), name='mobile-user-login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('verify', TokenVerifyView.as_view(), name='token_verify'),
    path('workers', WorkersView.as_view({'get': 'list', 'post': 'create'}), name='worker-list'),
    path('workers/<uuid>', WorkersView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='worker-details'),
    path('admins', AdminsViews.as_view({'get': 'list', 'post': 'create'}), name='admins-list'),
    path('admins/<uuid>', AdminsViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='admins-details'),
    path('users/<uuid>/change-password', ChangePasswordView.as_view(), name='change-password'),
    path('password/re-generate', PasswordReGenerateView.as_view(), name='password-re-generate'),
    path('generate-code', CodeGenerateByIDView.as_view(), name='generate-code-by-id'),
    path('verify-code', VerifyCodeAndCreateAccessTokenView.as_view(), name='verify-otp-code'),
    path('set-new-password', SetNewPasswordView.as_view(), name='set-new-password')
]
