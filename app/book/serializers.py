from rest_framework import serializers


class SeatAllotSerializer(serializers.Serializer):
    ticket = serializers.UUIDField()
    name = serializers.CharField(max_length=50)


class SeatAllotResponseSerializer(serializers.Serializer):
    ticket = serializers.UUIDField()
    name = serializers.CharField(max_length=50)
    seat_number = serializers.IntegerField()


class VacateSeatSerializer(serializers.Serializer):
    seat_number = serializers.IntegerField()
