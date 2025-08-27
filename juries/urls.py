from django.urls import path
from .views import JuryViewSet


urlpatterns = [
    path('login/juri/', JuryViewSet.as_view({"post": "login"}), name="login"),

]