from django.urls import path, include

from .views import occupySeat
urlpatterns = [
    path('occupy/', occupySeat.asView()),
    path('vacate/'),
    path('get_info/<str:pk>'),
]