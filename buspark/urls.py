from django.urls import path, include
from buspark.views import *


urlpatterns = [
    path('driver/', DriverListView.as_view()),
    path('driver/<int:pk>/', DriverDetailView.as_view()),
    path('bus/', BusListView.as_view()),
    path('driver/create/', DriverCreateView.as_view()),
    path('bus/create/', BusCreateView.as_view()),
    path('travel_driver/', TravelDriverListView.as_view()),
    path('travel_driver/<int:pk>/', TravelDriverDetailView.as_view()),
]