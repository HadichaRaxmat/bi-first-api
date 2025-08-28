from django.urls import path
from .views import Re

urlpatterns = [
    path('results/', ResultViewSet.as_view({'get': 'list'}), name='home_results'),
]