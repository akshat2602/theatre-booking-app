from rest_framework import permissions
from django.conf import settings
from .utils import is_number


class seatNumberCheckPermission(permissions.BasePermission):
    message = "Seat number doesn't exist!"

    def has_permission(self, request, view):
        if is_number(request.data['seat_number']):
            return settings.MAX_OCCUPANCY >= request.data['seat_number'] > 0
        return False
