from .views import Pa

urlpatterns = [
    path('payment/', PaymentViewSet.as_view({'post': 'create'}), name='competition-payment'),
]

