from django.conf import settings
from rest_framework import status, generics
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .serializers import SeatAllotSerializer, \
    SeatInfoResponseSerializer, \
    VacateSeatSerializer, \
    MessageSerializer, \
    AvailableSeatSerializer
from .permissions import seatNumberCheckPermission
from .utils import is_uuid, is_number, getInfoResponse

seats = dict.fromkeys(i for i in range(1, settings.MAX_OCCUPANCY + 1))


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


class vacateSeat(generics.DestroyAPIView):
    serializer_class = VacateSeatSerializer
    permission_classes = (seatNumberCheckPermission,)

    @swagger_auto_schema(request_body=VacateSeatSerializer,
                         responses={200: MessageSerializer})
    def delete(self, request, *args, **kwargs):
        """
        Request: Send seat number in request to vacate the seat
        Response: Return a message of success or failure
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if settings.MAX_OCCUPANCY >= serializer.data['seat_number']:
                if seats[serializer.data['seat_number']] is not None:
                    seats[serializer.data['seat_number']] = None
                    print(seats)
                    message = {
                        "message": "The provided seat number has been vacated!"
                    }
                    message_serializer = MessageSerializer(data=message)
                    message_serializer.is_valid()
                    return Response(data=message_serializer.data,
                                    status=status.HTTP_200_OK)
                else:
                    print(seats)
                    error_message = {
                        "message": "This seat number is vacant already!"
                    }
                    message_serializer = MessageSerializer(data=error_message)
                    message_serializer.is_valid()
                    return Response(data=message_serializer.data,
                                    status=status.HTTP_404_NOT_FOUND)

        return Response(data=serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

        elif is_number(pk):
            if int(pk) >= settings.MAX_OCCUPANCY or int(pk) <= 0:
                error_message = {
                    "message": "Seat number doesn't exist!"
                }
                serializer = MessageSerializer(data=error_message)
                serializer.is_valid()
                return Response(data=serializer.data,
                                status=status.HTTP_400_BAD_REQUEST)

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
