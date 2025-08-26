from .views import PaymentViewSet
from django.urls import path

urlpatterns = [
    path('payment/', PaymentViewSet.as_view({'post': 'create'}), name='payment'),
]

