from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import SeatAllotSerializer, \
    SeatAllotResponseSerializer, \
    VacateSeatSerializer

seats = dict.fromkeys(i for i in range(1, settings.MAX_OCCUPANCY + 1))


class occupySeat(generics.CreateAPIView):
    serializer_class = SeatAllotSerializer

    def create(self, request, *args, **kwargs):
        if seats[settings.MAX_OCCUPANCY] is not None:
            return Response(data={"Message": "Theatre is fully occupied!"})

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data['name']
            ticket = serializer.data['ticket']
            seat_number = 0
            for key, values in seats.items():
                if seats[key] is not None:
                    if seats[key]['ticket'] == ticket:
                        return Response(data={
                            "Message": "A ticket with this UUID has already been booked!"
                        })
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
            response_serializer = SeatAllotResponseSerializer(
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

    def delete(self, request, *args, **kwargs):
        seat_number = request.data['seat_number']
        if settings.MAX_OCCUPANCY >= seat_number:
            if seats[seat_number]:
                seats[seat_number] = None
                print(seats)
                return Response(data={
                    "Message": "The provided seat number has been vacated!"
                }, status=status.HTTP_204_NO_CONTENT)
            else:
                print(seats)
                return Response(data={
                    "Message": "The provided seat number is vacant already!"
                }, status=status.HTTP_404_NOT_FOUND)
        print(seats)
        return Response(data={
            "Message": "Seat number doesn't exist!"
        }, status=status.HTTP_404_NOT_FOUND)
