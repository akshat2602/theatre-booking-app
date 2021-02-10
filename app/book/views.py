from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import SeatSerializer, ResponseSerializer

seats = dict.fromkeys(i for i in range(settings.MAX_OCCUPANCY))


class occupySeat(generics.CreateAPIView):
    serializer_class = SeatSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        ticket = serializer.data['ticket']
        seat_number = 0
        for key, values in seats:
            if seats[key] is not None:
                pass
            else:
                seats[key] = ticket
                seat_number = key
                break
        response_serializer = ResponseSerializer(ticket=serializer.data['ticket'],
                                                 name=serializer.data['name'],
                                                 seat_number=seat_number)
        if response_serializer.validate():
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(response_serializer.errors, status=status.HTTP_404_NOT_FOUND)
