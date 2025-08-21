from django.urls import path
from .views import CompetitionViewSet, ApplicationViewSet

urlpatterns = [
    path('get_competition/', CompetitionViewSet.as_view({'get': 'list'}), name='competition'),
    # ApplicationViewSet
    path('applications/', ApplicationViewSet.as_view({'get': 'list', 'post': 'create'}), name='application-list'),
    path('applications/<int:pk>/', ApplicationViewSet.as_view({'get': 'retrieve'}), name='application-detail'),
]