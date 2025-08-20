from django.urls import path
from .views import AuthViewSet, EmailVerificationViewSet

urlpatterns = [
    path("register/", AuthViewSet.as_view({"post": "register"}), name="register"),
    path('email_verification/', EmailVerificationViewSet.as_view({'post': 'post'}), name='email_verification'),
    path("email_verification/resend/", EmailVerificationViewSet.as_view({"post": "resend"}), name="email_verification_resend"),
    path("login/", AuthViewSet.as_view({"post": "login"}), name="login"),
]
