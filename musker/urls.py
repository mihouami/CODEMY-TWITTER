from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("check_meep/", check_meep, name="check_meep"),
]
