from django.urls import path
from .views import (HomeViewSet, ContactUsViewSet, SubscribeViewSet, LocationViewSet, ContactNumberViewSet, SocialMediaViewSet,
                   PolicyViewSet)

urlpatterns = [
    path('get_header/', HomeViewSet.as_view({'get': 'header'}), name='home_header'),
    path('get_contact_us/', ContactUsViewSet.as_view({'get': 'list'}), name='home_contact_us'),
    path('subscribe/', SubscribeViewSet.as_view({'post': 'create'}), name='home_subscribe'),
    path('get_locations/', LocationViewSet.as_view({'get': 'list'}), name='home_location'),
    path('get_contact_numbers/', ContactNumberViewSet.as_view({'get': 'list'}), name='home_contact_numbers'),
    path('get_social_media/', SocialMediaViewSet.as_view({'get': 'list'}), name='home_social_media'),
    path('results/', ResultViewSet.as_view({'get': 'list'}), name='home_results'),
    path('policy/', PolicyViewSet.as_view({'get': 'list'}), name='home_policy')

]