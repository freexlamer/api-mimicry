from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


from . import serializers
from core import models


class FeedViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()


class RentalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RentalSerializer
    queryset = models.Rental.objects.all()
    event_model = models.Event

    def _create_event(self, event_type, rental):
        return self.event_model.objects.create(rental=rental, type=event_type)

    @action(
        detail=True,
        methods=['post'],
        parser_classes=(FileUploadParser,),
    )
    def upload_img(self, request, pk=None):
        rent = self.get_object()
        image = request.data['file']
        print(image.file)
        print(image.name)
        rent.image = image

        rent.save(update_fields=['image'])
        return Response({'status': 'Image accepted.'},
                        status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        obj = self.queryset.get(id=pk)
        if obj.is_free:
            self._create_event(self.event_model.VIEW, obj)
            return Response({'status': 'View accepted.'},
                            status=status.HTTP_202_ACCEPTED)

        return Response({'status': 'View denied.'},
                        status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def checkin(self, request, pk=None):
        obj = self.queryset.get(id=pk)
        if obj.is_free:
            self._create_event(self.event_model.CHECK_IN, obj)
            obj.is_free = False
            obj.save(update_fields=['is_free'])
            return Response({'status': 'Checkin accepted.'},
                            status=status.HTTP_202_ACCEPTED)

        return Response({'status': 'Checkin denied.'},
                        status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        obj = self.queryset.get(id=pk)
        if not obj.is_free:
            self._create_event(self.event_model.CHECK_OUT, obj)
            obj.is_free = True
            obj.save(update_fields=['is_free'])
            return Response({'status': 'Checkout accepted.'},
                            status=status.HTTP_202_ACCEPTED)

        return Response({'status': 'Checkout denied.'},
                        status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def payment(self, request, pk=None):
        obj = self.queryset.get(id=pk)
        if not obj.is_free:
            self._create_event(self.event_model.PAYMENT, obj)
            return Response({'status': 'Payment accepted.'},
                            status=status.HTTP_202_ACCEPTED)

        return Response({'status': 'Payment denied.'},
                        status=status.HTTP_403_FORBIDDEN)
