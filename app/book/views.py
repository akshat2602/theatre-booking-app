from django.conf import settings
from rest_framework import status, generics
from rest_framework.response import Response
from uuid import UUID
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .serializers import SeatAllotSerializer, \
    SeatInfoResponseSerializer, \
    VacateSeatSerializer, \
    MessageSerializer, \
    AvailableSeatSerializer
from .permissions import seatNumberCheckPermission

seats = dict.fromkeys(i for i in range(1, settings.MAX_OCCUPANCY + 1))


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


class occupySeat(generics.CreateAPIView):
    serializer_class = SeatAllotSerializer

    @swagger_auto_schema(responses={201: SeatInfoResponseSerializer})
    def post(self, request, *args, **kwargs):
        """
        Request: Send ticket id and name to book a seat
        Response: Returns ticket id, name and seat number if success
        """
        serializer = self.serializer_class(data=request.data)
        if seats[settings.MAX_OCCUPANCY] is not None:
            error_message = {
                "message": "Theatre is fully occupied!"
            }
            serializer = MessageSerializer(data=error_message)
            serializer.is_valid()
            return Response(data=serializer.data,
                            status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            name = serializer.data['name']
            error_message = {
                "message": "A ticket with this UUID has already been booked!"
            }
            ticket = serializer.data['ticket']
            seat_number = 0
            for key, values in seats.items():
                if seats[key] is not None:
                    if seats[key]['ticket'] == ticket:
                        serializer = MessageSerializer(data=error_message)
                        serializer.is_valid()
                        return Response(data=serializer.data,
                                        status=status.HTTP_409_CONFLICT)
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


class vacateSeat(APIView):
    serializer_class = VacateSeatSerializer
    permission_classes = (seatNumberCheckPermission,)

    @swagger_auto_schema(request_body=VacateSeatSerializer,
                         responses={200: MessageSerializer})
    def delete(self, request, *args, **kwargs):
        """
        Request: Send seat number in request to vacate the seat
        Response: Return a message of success or failure
        """
        seat_number = request.data['seat_number']
        if settings.MAX_OCCUPANCY >= seat_number:
            if seats[seat_number]:
                seats[seat_number] = None
                print(seats)
                message = {
                    "message": "The provided seat number has been vacated!"
                }
                serializer = MessageSerializer(data=message)
                serializer.is_valid()
                return Response(data=serializer.data,
                                status=status.HTTP_200_OK)
            else:
                print(seats)
                error_message = {
                    "message": "The provided seat number is vacant already!"
                }
                serializer = MessageSerializer(data=error_message)
                serializer.is_valid()
                return Response(data=serializer.data,
                                status=status.HTTP_404_NOT_FOUND)


class getInfo(APIView):
    serializer_class = SeatInfoResponseSerializer

    @swagger_auto_schema(responses={200: SeatInfoResponseSerializer})
    def get(self, request, pk):
        """
        PK: Send seat number or ticket id or name in request to get seat info
        Request: Nothing expected in request
        Response: Return serializer with seat information
        """
        if is_uuid(pk):
            error_message = {
                "message": "No seat is booked with the provided ticket ID!"
            }
            serializer = MessageSerializer(data=error_message)
            serializer.is_valid()
            for key, value in seats.items():
                if seats[key] is not None:
                    if seats[key]['ticket'] == pk:
                        resp = getInfoResponse(ticket=pk,
                                               name=seats[key]['name'],
                                               seat_number=key)
                        print(resp)
                        return resp

            print(seats)
            return Response(data=serializer.data,
                            status=status.HTTP_404_NOT_FOUND)

        elif pk.isnumeric():
            if int(pk) >= settings.MAX_OCCUPANCY:
                error_message = {
                    "message": "Seat number doesn't exist!"
                }
                serializer = MessageSerializer(data=error_message)
                serializer.is_valid()
                return Response(data=serializer.data,
                                status=status.HTTP_404_NOT_FOUND)

            error_message = {
                "message": "No seat is booked with this seat number"
            }
            serializer = MessageSerializer(data=error_message)
            serializer.is_valid()
            for key, value in seats.items():
                if key == int(pk) and seats[key] is not None:
                    resp = getInfoResponse(ticket=seats[key]['ticket'],
                                           name=seats[key]['name'],
                                           seat_number=pk)
                    print(resp)
                    return resp

            print(seats)
            return Response(data=serializer.data,
                            status=status.HTTP_404_NOT_FOUND)

        else:
            error_message = {
                "message": "No seat is booked with the provided name!"
            }
            serializer = MessageSerializer(data=error_message)
            serializer.is_valid()
            for key, value in seats.items():
                if seats[key] is not None:
                    if seats[key]['name'] == pk:
                        resp = getInfoResponse(ticket=seats[key]['ticket'],
                                               name=pk,
                                               seat_number=key)
                        print(resp)
                        return resp

            print(seats)
            return Response(data=serializer.data,
                            status=status.HTTP_404_NOT_FOUND)


class getEmptySeat(APIView):
    serializer_class = AvailableSeatSerializer

    @swagger_auto_schema(responses={200: AvailableSeatSerializer})
    def get(self, request):
        """
        Request: Nothing expected in request
        Response: Return serializer with number of seats available for booking
        """
        counter = 0
        for key, value in seats.items():
            if seats[key] is not None:
                counter += 1

        number_of_seats = settings.MAX_OCCUPANCY - counter
        available_seats = {
            "seats": number_of_seats
        }
        print("Number of available seats are: ", number_of_seats)
        serializer = AvailableSeatSerializer(data=available_seats)
        if serializer.is_valid():
            return Response(data=serializer.data,
                            status=status.HTTP_200_OK)

        return Response(data=serializer.errors,
                        status=status.HTTP_404_NOT_FOUND)
