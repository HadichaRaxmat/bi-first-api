from django.urls import path
from .views import ExpertViewSet

urlpatterns = [
    path('experts/', ExpertViewSet.as_view({'get': 'list'}), name='experts'),
]
