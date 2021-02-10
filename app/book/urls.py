from django.urls import path, include

from .views import occupySeat, vacateSeat
urlpatterns = [
    path('occupy/', occupySeat.as_view()),
    path('vacate/', vacateSeat.as_view()),
    # path('get_info/<str:pk>'),
]