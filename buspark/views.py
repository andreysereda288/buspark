from rest_framework import generics
from buspark.serializers import DriverSerializer, BusSerializer, TravelDriverSerializer
from buspark.models import Driver, Bus
from buspark.calculation import get_distance
from rest_framework.response import Response
from django.db.models import Max
import math


class DriverListView(generics.ListAPIView):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class TravelDriverListView(generics.ListAPIView):
    serializer_class = TravelDriverSerializer
    queryset = Driver.objects.filter(bus__velocity__gt=0)\
        .annotate(max_velocity=Max('bus__velocity')).order_by('-max_velocity')

    def list(self, request, *args, **kwargs):
        point1 = request.GET.get('from', '')
        point2 = request.GET.get('to')
        distance_response = get_distance(start=point1, finish=point2)
        queryset = self.filter_queryset(self.get_queryset())
        for item in queryset:
            item_velocity = item.bus.aggregate(Max('velocity'))['velocity__max']
            if distance_response['distance']:
                item.travel_time = int(math.ceil(0.001*distance_response['distance']/item_velocity/8))
            else:
                item.travel_time = distance_response['status_message']


        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class TravelDriverDetailView(generics.RetrieveAPIView):
    serializer_class = TravelDriverSerializer
    queryset = Driver.objects.all()

    def retrieve(self, request, *args, **kwargs):
        point1 = request.GET.get('from')
        point2 = request.GET.get('to')
        distance_response = get_distance(start=point1, finish=point2)
        print(distance_response)
        instance = self.get_object()
        instance_velocity = instance.bus.aggregate(Max('velocity'))['velocity__max']
        if distance_response['distance']:
            instance.travel_time = int(math.ceil(0.001*distance_response['distance']/instance_velocity/8))
        else:
            instance.travel_time = distance_response['status_message']
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()


class BusListView(generics.ListAPIView):
    serializer_class = BusSerializer
    queryset = Bus.objects.all()


class DriverCreateView(generics.CreateAPIView):
    serializer_class = DriverSerializer


class BusCreateView(generics.CreateAPIView):
    serializer_class = BusSerializer
