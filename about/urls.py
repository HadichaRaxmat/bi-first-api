from django.urls import path
from .views import AboutViewSet

urlpatterns = [
    path('about/', AboutViewSet.as_view({'get': 'list'}), name='about'),
]
