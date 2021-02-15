from rest_framework import serializers


# Serializer for taking input for occupy seat endpoint
class SeatAllotSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    ticket = serializers.UUIDField()
    name = serializers.CharField(max_length=50)


# Serializer for returning output for occupy seat endpoint or get_info endpoint
class SeatInfoResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    ticket = serializers.UUIDField()
    name = serializers.CharField(max_length=50)
    seat_number = serializers.IntegerField()


# Serializer for taking input for vacate seat endpoint
class VacateSeatSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    seat_number = serializers.IntegerField()


# Serializer for taking displaying error or success messages in response
class MessageSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    message = serializers.CharField(max_length=200)


class AvailableSeatSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    seats = serializers.IntegerField()
