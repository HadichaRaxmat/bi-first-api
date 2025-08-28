from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response

from .serializers import (HeaderSerializer, ContactUsSerializer, SubscribeSerializer, LocationSerializer, ContactNumberSerializer,
                          SocialMediaSerializer)

from drf_yasg.utils import swagger_auto_schema
from .models import Header, ContactUs, Location, ContactNumber, SocialMedia


class HomeViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get Header",
        operation_summary="Get Header",
        responses={
            200: HeaderSerializer(),
        },
        tags=['home']
    )
    def header(self, request, *args, **kwargs):
        headers = Header.objects.all().first()
        serializer = HeaderSerializer(headers, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




class ContactUsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get contact us",
        operation_summary="Get contact us",
        responses={
            200: ContactUsSerializer(),
        },
        tags=['home']
    )
    def list(self, request):
        queryset = ContactUs.objects.all()
        serializer = ContactUsSerializer(queryset, many=True)
        return Response(serializer.data)


class SubscribeViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Create subscribe",
        operation_summary="Create subscribe",
        responses={
            200: SubscribeSerializer(),
        },
        tags=['home']
    )
    def create(self, request):
        serializer = SubscribeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="List locations",
        operation_summary="List locations",
        responses={
            200: LocationSerializer(),
        },
        tags=['home']
    )
    def list(self, request):
        queryset = Location.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)


class ContactNumberViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="List contact numbers",
        operation_summary="List contact numbers",
        responses={200: ContactNumberSerializer(many=True)},
        tags=['home']
    )
    def list(self, request):
        queryset = ContactNumber.objects.all()
        serializer = ContactNumberSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class SocialMediaViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="List Social Media",
        operation_summary="List Social Media",
        responses={200: SocialMediaSerializer(many=True)},
        tags=['home']
    )
    def list(self, request):
        social_media = SocialMedia.objects.all()
        serializer = SocialMediaSerializer(social_media, many=True)
        return Response(serializer.data)

