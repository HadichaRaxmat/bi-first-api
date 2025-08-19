from django.urls import path
from .views import AddChildrenViewSet

urlpatterns = [
    path('children/', AddChildrenViewSet.as_view({'get': 'list', 'post': 'create'}), name='children-list'),
    path('child/<int:pk>/', AddChildrenViewSet.as_view({'delete': 'destroy',}), name='children-detail')
]