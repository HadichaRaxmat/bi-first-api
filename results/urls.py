from django.urls import path
from .views import ResultViewSet

urlpatterns = [
    path('results/', ResultViewSet.as_view({'get': 'list'}), name='results'),
]