from rest_framework import serializers


class SeatAllotSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    ticket = serializers.UUIDField()
    name = serializers.CharField(max_length=50)


class SeatInfoResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    ticket = serializers.UUIDField()
    name = serializers.CharField(max_length=50)
    seat_number = serializers.IntegerField()


class VacateSeatSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    seat_number = serializers.IntegerField()
