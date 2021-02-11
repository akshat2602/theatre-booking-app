from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from uuid import UUID
from .serializers import SeatAllotSerializer, \
    SeatInfoResponseSerializer, \
    VacateSeatSerializer
from .permissions import seatNumberCheckPermission

seats = dict.fromkeys(i for i in range(1, settings.MAX_OCCUPANCY + 1))


class occupySeat(generics.CreateAPIView):
    serializer_class = SeatAllotSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if seats[settings.MAX_OCCUPANCY] is not None:
            error_message = "Theatre is fully occupied!"
            return Response(data={
                "Message": error_message
            }, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            name = serializer.data['name']
            error_message = "A ticket with this UUID has already been booked!"
            ticket = serializer.data['ticket']
            seat_number = 0
            for key, values in seats.items():
                if seats[key] is not None:
                    if seats[key]['ticket'] == ticket:
                        return Response(data={
                            "Message": error_message
                        }, status=status.HTTP_409_CONFLICT)
                    else:
                        pass
                else:
                    seats[key] = {"ticket": ticket, "name": name}
                    seat_number = key
                    break
            print("Seat number allotted is: ", str(seat_number))
            data = {
                "ticket": serializer.data['ticket'],
                "name": serializer.data['name'],
                "seat_number": seat_number,
            }
            print(seats)
            response_serializer = SeatInfoResponseSerializer(
                data=data
            )
            if response_serializer.is_valid():
                return Response(response_serializer.data,
                                status=status.HTTP_201_CREATED)

            return Response(response_serializer.errors,
                            status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors,
                        status=status.HTTP_404_NOT_FOUND)


class vacateSeat(generics.DestroyAPIView):
    serializer_class = VacateSeatSerializer
    permission_classes = (seatNumberCheckPermission,)

    def delete(self, request, *args, **kwargs):
        seat_number = request.data['seat_number']
        if settings.MAX_OCCUPANCY >= seat_number:
            if seats[seat_number]:
                seats[seat_number] = None
                print(seats)
                error_message = "The provided seat number has been vacated!"
                return Response(data={
                    "Message": error_message
                }, status=status.HTTP_204_NO_CONTENT)
            else:
                print(seats)
                error_message = "The provided seat number is vacant already!"
                return Response(data={
                    "Message": error_message
                }, status=status.HTTP_404_NOT_FOUND)


def is_uuid(string):
    try:
        uuid_object = UUID(string, version=4)
    except ValueError:
        return False
    return str(uuid_object) == string


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


class getInfo(generics.RetrieveAPIView):

    def retrieve(self, request, pk, *args, **kwargs):
        if is_uuid(pk):
            error_message = "No seat is booked with the provided ticket ID!"
            for key, value in seats.items():
                if seats[key] == pk:
                    resp = getInfoResponse(ticket=pk,
                                           name=seats[key]['name'],
                                           seat_number=key)
                    return resp

                return Response(data={
                    "Message": error_message
                }, status=status.HTTP_404_NOT_FOUND)

        elif type(pk) == int or type(pk) == float:
            error_message = ""
            for key, value in seats.items():
                if key == pk:
                    resp = getInfoResponse(ticket=seats[key]['ticket'],
                                           name=seats[key]['name'],
                                           seat_number=pk)
                    return resp

            return Response(data={
                "Message": error_message
            }, status=status.HTTP_404_NOT_FOUND)

        else:
            error_message = "No seat is booked with the provided name!"
            for key, value in seats.items():
                if seats[key]['name'] == pk:
                    resp = getInfoResponse(ticket=seats[key]['ticket'],
                                           name=pk,
                                           seat_number=key)
                    return resp

            return Response(data={
                    "Message": error_message
                }, status=status.HTTP_404_NOT_FOUND)
