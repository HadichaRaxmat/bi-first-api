from django.urls import path
from .views import HomeViewSet

urlpatterns = [
    path('get_header/', HomeViewSet.as_view({'get': 'header'}), name='home_header'),
]