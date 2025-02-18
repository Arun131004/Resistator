from django.urls import path
from .views import resistor_home, calculate_resistance

urlpatterns = [
    path("", resistor_home, name="resistor_home"),
    path("calculate/", calculate_resistance, name="calculate_resistance"),
]
