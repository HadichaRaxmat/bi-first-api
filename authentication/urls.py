from django.urls import path
from .views import AuthViewSet, EmailVerificationViewSet, AccountViewSet

urlpatterns = [
    path("register/", AuthViewSet.as_view({"post": "register"}), name="register"),
    path('email_verification/', EmailVerificationViewSet.as_view({'post': 'post'}), name='email_verification'),
    path("email_verification/resend/", EmailVerificationViewSet.as_view({"post": "resend"}), name="email_verification_resend"),
    path("login/", AuthViewSet.as_view({"post": "login"}), name="login"),
    path("profile/", PersonalInfoViewSet.as_view({"get": "get", "patch": "update"}), name="profile"),
    path('profile/', AccountViewSet.as_view({"get": "get", "patch": "update"}), name="profile"),
    path('change_password/', AccountViewSet.as_view({"post": "change_password"}), name="change_password"),
    path('delete_account/', AccountViewSet.as_view({"post": "delete"}), name="delete_account"),
]
