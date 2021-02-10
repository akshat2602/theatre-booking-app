from rest_framework import serializers


class SeatSerializer(serializers.Serializer):
    ticket = serializers.UUIDField()
    name = serializers.CharField(max_length=50)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

class ResponseSerializer(serializers.Serializer):
    ticket = serializers.UUIDField()
    name = serializers.CharField(max_length=50)
    seat_number = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass