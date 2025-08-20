from django.urls import path
from .views import GalleryViewSet

urlpatterns = [
    path('galleries/', GalleryViewSet.as_view({'get': 'list'}), name='gallery-list'),
]
