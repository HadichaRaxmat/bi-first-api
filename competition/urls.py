from django.urls import path
from .views import CompetitionViewSet

urlpatterns = [
    path('get_competition/', CompetitionViewSet.as_view({'get': 'get'}), name='competition'),
]