from django.urls import path
from .views import occupySeat, \
    vacateSeat, \
    getInfo, \
    getEmptySeat

urlpatterns = [
    path('occupy/', occupySeat.as_view(), name="occupy_seat"),
    path('vacate/', vacateSeat.as_view(), name="vacate_seat"),
    path('get_info/<str:pk>', getInfo.as_view(), name="get_info"),
    path('get_empty_seats/', getEmptySeat.as_view(), name="get_empty_seats")
]
