from uuid import UUID
from rest_framework.response import Response
from .serializers import SeatInfoResponseSerializer
from rest_framework import status


def is_uuid(string):
    try:
        uuid_object = UUID(string, version=4)
    except ValueError:
        return False
    return str(uuid_object) == string


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def getInfoResponse(ticket, name, seat_number):
    serializer = SeatInfoResponseSerializer(
        data={
            "seat_number": seat_number,
            "ticket": ticket,
            "name": name
        })
    if serializer.is_valid():
        return Response(data=serializer.data,
                        status=status.HTTP_302_FOUND)
    return Response(data=serializer.errors,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
