from django.urls import path
from .views import ChildrenViewSet

urlpatterns = [
    path('children/', ChildrenViewSet.as_view({'get': 'list', 'post': 'create'}), name='children-list'),
    path('child/<int:pk>/', ChildrenViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='children-detail'),
]
