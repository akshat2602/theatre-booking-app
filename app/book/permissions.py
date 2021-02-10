from rest_framework import permissions
from django.conf import settings


class seatNumberCheckPermission(permissions.BasePermission):
    message = "Seat number doesn't exist!"

    def has_permission(self, request, view):
        return settings.MAX_OCCUPANCY >= request.data['seat_number']
