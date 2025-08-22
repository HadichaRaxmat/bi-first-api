from django.urls import path
from .views import CompetitionViewSet, ApplicationViewSet

urlpatterns = [
    # Список конкурсов
    path('get_competition/', CompetitionViewSet.as_view({'get': 'list'}), name='competition'),

    # Заявки
    path('applications/', ApplicationViewSet.as_view({'get': 'list', 'post': 'create'}), name='application-list'),
    path('applications/<int:pk>/', ApplicationViewSet.as_view({'get': 'retrieve'}), name='application-detail'),

    # Подписки (GET — список, POST — подписка)
    path('applications/subscriptions/', ApplicationViewSet.as_view({'get': 'subscriptions', 'post': 'subscribe'}), name='subscriptions'),
]
