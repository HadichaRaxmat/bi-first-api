from django.urls import path
from .views import CompetitionViewSet, ApplicationViewSet, CompetitionPaymentViewSet

urlpatterns = [
    # Список конкурсов
    path('get_competition/', CompetitionViewSet.as_view({'get': 'list'}), name='competition'),

    # Заявки
    path('applications/', ApplicationViewSet.as_view({'post': 'create'}), name='application-list'),

    # POST — подписка)
    path('applications/subscription/', ApplicationViewSet.as_view({'post': 'subscribe'}), name='application-subscribe'),

    # post - payment
    path('competition/payment/', CompetitionPaymentViewSet.as_view({'post': 'create'}), name='competition-payment'),
]
